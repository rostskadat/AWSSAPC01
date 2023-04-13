const express = require('express');
const fileUpload = require('express-fileupload');
const bodyParser = require('body-parser');
const { promisify } = require("util");
const log4js = require("log4js");
const mysql = require('mysql');
const path = require('path');
const AWS = require('aws-sdk');
const redis = require("redis");
const nunjucks = require('nunjucks');

const app = express();


const PORT = process.env.PORT || 80;
const REGION = process.env.REGION;
const SECRET_ARN = process.env.SECRET_ARN;

if (REGION == null) {
    throw 'Missing REGION environment variable!';
}
if (SECRET_ARN == null) {
    throw 'Missing SECRET_ARN environment variable!';
}

const RDS_HOST = process.env.RDS_HOST;
const RDS_PORT = process.env.RDS_PORT || 3306;
if (RDS_HOST == null) {
    throw 'Missing RDS_HOST environment variable!';
}

const REDIS_HOST = process.env.REDIS_HOST;
const REDIS_PORT = process.env.REDIS_PORT || 6379;
global.hasCacheLayer = false
if (REDIS_HOST != null) {
    hasCacheLayer = true
}

const logger = log4js.getLogger();
logger.level = process.env.LOG4JS_LEVEL || "error";

// import { getHomePage } from './routes/home.js';
const { getHomePage } = require('./routes/home');
const { getHealthPage } = require('./routes/health');
const { getErrorPage } = require('./routes/error');
const { addItemPage, addItem, deleteItem, editItem, editItemPage } = require('./routes/item');

// Let's setup a few things for the app
app.set('port', PORT); // set express to use this port
app.set('views', __dirname + '/views'); // set express to look in this folder to render our view
nunjucks.configure(app.get('views'), {
    autoescape: true,
    express: app,
    noCache: true
});
app.set('view engine', 'html');
// app.set('view engine', 'ejs'); // configure template engine
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // parse form data client
app.use(express.static(path.join(__dirname, 'public'))); // configure express to use public folder
app.use(fileUpload()); // configure fileupload

// routes for the app
app.get('/', getHomePage);
app.get('/health', getHealthPage);
app.get('/error', getErrorPage)
app.get('/add', addItemPage);
app.post('/add', addItem);
app.get('/delete/:id', deleteItem);
app.get('/edit/:id', editItemPage);
app.post('/edit/:id', editItem);

// Retrieve the Secret...
var client = new AWS.SecretsManager({ region: REGION });
client.getSecretValue({ SecretId: SECRET_ARN }).promise().then((data) => {
    if (!'SecretString' in data) {
        throw 'Can only handle SecretString secrets.';
    }
    var secret = JSON.parse(data.SecretString);
    logger.debug("Connecting to DB " + secret.username + "@" + RDS_HOST + ":" + RDS_PORT + "/" + secret.dbname + " ...");
    const db = mysql.createConnection({
        host: RDS_HOST,
        port: RDS_PORT,
        user: secret.username,
        password: secret.password,
        database: secret.dbname
    });
    // connect to database
    db.connect((err) => {
        if (err) {
            throw err;
        }
        logger.info("Connected to DB '" + RDS_HOST + "'");
    });
    global.db = db;

    if (hasCacheLayer) {
        var url = "rediss://" + REDIS_HOST + ":" + REDIS_PORT
        logger.debug(`Connecting to Cache ${REDIS_HOST}:${REDIS_PORT} ...`);
        const cache = redis.createClient({ url: url });
        cache.on("error", (err) => {
            throw err;
        })
        cache.on("ready", () => {
            logger.info("Connected to Cache '" + REDIS_HOST + "'");
            global.cache = cache;
        });
    }

    app.listen(PORT, () => {
        logger.info(`Server running on port: ${PORT}`);
    });
}).catch((err) => {
    // Can't even connect to the DB. Exit without further adieu
    logger.error(err);
});
