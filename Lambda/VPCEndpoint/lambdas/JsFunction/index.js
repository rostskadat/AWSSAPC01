// Ref: https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html

const axios = require('axios');
const AWS = require('aws-sdk')
const path = require('path')

var AWSXRay = require('aws-xray-sdk-core')
var captureMySQL = require('aws-xray-sdk-mysql')
var mysql = captureMySQL(require('mysql2'))
const { promisify } = require('util')

const log4js = require("log4js");
const logger = log4js.getLogger();
logger.level = process.env.LOG4JS_LEVEL || "debug";

const PUBLIC_URL = 'https://www.bbc.com/';
const REGION = process.env.REGION;
const SECRET_ARN = process.env.SECRET_ARN;
const PUBLIC_TABLE = process.env.PUBLIC_TABLE;
const PRIVATE_TABLE = process.env.PRIVATE_TABLE;

if (REGION == null) {
    throw 'Missing REGION environment variable!';
}
if (SECRET_ARN == null) {
    throw 'Missing SECRET_ARN environment variable!';
}
if (PUBLIC_TABLE == null) {
    throw 'Missing PUBLIC_TABLE environment variable!';
}
if (PRIVATE_TABLE == null) {
    throw 'Missing PRIVATE_TABLE environment variable!';
}

var secretsManager = new AWS.SecretsManager({ region: REGION });
var dynamoDb = new AWS.DynamoDB({ apiVersion: '2012-08-10' });

// The idea is to concurrently call our 4 endpoints:
// - PUBLIC_URL
// - PRIVATE_TABLE
// - PUBLIC_TABLE
// - RDS
// gather all the result and return them

async function get_url() {
    console.info("get_url ("+PUBLIC_URL+") ...");
    const response = await axios.get(PUBLIC_URL)
    return response.data.length
}

async function get_item(tableName) {
    console.info("get_item ("+tableName+") ...");
    var params = {
        TableName: tableName,
        Key: {
            'id': { S: '1' }
        }
    };
    const data = await dynamoDb.getItem(params).promise();
    return data.Item;
}

async function get_rds() {
    console.info("get_rds ("+SECRET_ARN+") ...");
    var data = await secretsManager.getSecretValue({ SecretId: SECRET_ARN }).promise()
    var secret = JSON.parse(data.SecretString);
    console.info("Connecting to " + secret.username + "@" + secret.host + ":" + secret.port + "/" + secret.dbname + " ...");
    const connection = await mysql.createConnection({
        host: secret.host,
        port: secret.port,
        user: secret.username,
        password: secret.password,
        database: secret.dbname
    });
    console.info("Connected. Executing query ...")
    const [rows, fields] = await connection.execute('select ? + ? as sum', [2, 2]);
    console.info("Query executed")
    await connection.end();
    for (var row in rows) {
        console.info(rows[row]);
    }
    return rows
}

exports.handler = async (event, context) => {
    console.info("Starting Promise.allSettled() ...");
    const [url, private_table, public_table, rds] = await Promise.allSettled([
        get_url(),
        get_item(PRIVATE_TABLE),
        get_item(PUBLIC_TABLE),
        get_rds()
    ]);
    console.info("All promised settled");

    return {
        "statusCode": 200,
        "headers": {
            //  In order to configure CORS while using Lambda Proxy integration 
            //  it is important to add the following header (no set by
            //  APIGateway... )
            //  "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        // "isBase64Encoded": false,
        // "multiValueHeaders": {
        //     "X-Custom-Header": ["My value", "My other value"],
        // },
        "body": JSON.stringify({
            "url": url,
            "private_table": private_table,
            "public_table": public_table,
            "rds": rds,
        })
    }
}
