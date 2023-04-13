const express = require('express');
const fileUpload = require('express-fileupload');
const bodyParser = require('body-parser');
const log4js = require("log4js");
const mysql = require('mysql');
const path = require('path');
const AWS = require('aws-sdk');
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

const { getHomePage } = require('./routes/index');
const { getHealth } = require('./routes/health');
const { addPlayerPage, addPlayer, deletePlayer, editPlayer, editPlayerPage } = require('./routes/player');

const logger = log4js.getLogger();
logger.level = process.env.LOG4JS_LEVEL || "error";

var client = new AWS.SecretsManager({ region: REGION });

// Retrieve the Secret...
client.getSecretValue({ SecretId: SECRET_ARN }, function (err, data) {
    if (err || ! 'SecretString' in data ) {
        throw err;
    }
    var secret = JSON.parse(data.SecretString);

    logger.debug("Connecting to "+secret.username+"@"+secret.host+":"+secret.port+"/"+secret.dbname+" ...");
    const db = mysql.createConnection({
        host: secret.host,
        port: secret.port,
        user: secret.username,
        password: secret.password,
        database: secret.dbname
    });
    // connect to database
    db.connect((err) => {
        if (err) {
            throw err;
        }
        logger.info("Connected to '"+secret.dbInstanceIdentifier+"'");
    });
    global.db = db;

    // configure middleware
    app.set('port', PORT); // set express to use this port
    app.set('views', __dirname + '/views'); // set express to look in this folder to render our view
    app.set('view engine', 'ejs'); // configure template engine
    app.use(bodyParser.urlencoded({ extended: false }));
    app.use(bodyParser.json()); // parse form data client
    app.use(express.static(path.join(__dirname, 'public'))); // configure express to use public folder
    app.use(fileUpload()); // configure fileupload

    // routes for the app
    app.get('/', getHomePage);
    app.get('/health', getHealth);
    app.get('/add', addPlayerPage);
    app.get('/edit/:id', editPlayerPage);
    app.get('/delete/:id', deletePlayer);
    app.post('/add', addPlayer);
    app.post('/edit/:id', editPlayer);
    app.listen(PORT, () => {
        logger.info(`Server running on port: ${PORT}`);
    });
});



