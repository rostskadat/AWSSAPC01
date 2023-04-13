const { getLogger } = require("log4js");
const { basename } = require('path')

module.exports = {
    getHomePage: (req, res) => {
        const logger = getLogger(basename(__filename));
        // const rows = await db.query('SELECT * FROM `items` ORDER BY id ASC');
        let query = "SELECT * FROM `items` ORDER BY id ASC";
        db.query(query, (err, result) => {
            if (err) {
                logger.error(err);
                res.redirect('/error');
            }
            res.render('index.html', {
                title: 'View Items',
                items: result
            });
        });
    }
}