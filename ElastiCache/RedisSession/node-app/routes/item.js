const { getLogger } = require("log4js");
const { basename } = require('path')
const { unlink, existsSync } = require('fs');
const { v4: uuidv4 } = require('uuid');
const { promisify } = require("util");

module.exports = {

    addItemPage: (req, res) => {
        res.render('add-item.html', {
            title: 'Add a new item',
            message: '',
            item: {}
        });
    },
    addItem: (req, res) => {
        if (!req.files) {
            return res.status(400).send("No files were uploaded.");
        }

        let message = '';
        let description = req.body.description;
        let uploadedFile = req.files.image;
        let image_name = uploadedFile.name;
        let fileExtension = uploadedFile.mimetype.split('/')[1];
        image_name = uuidv4() + '.' + fileExtension;

        // check the filetype before uploading it
        if (uploadedFile.mimetype === 'image/png' || uploadedFile.mimetype === 'image/jpeg' || uploadedFile.mimetype === 'image/gif') {
            // upload the file to the /public/assets/img directory
            uploadedFile.mv(`public/assets/img/${image_name}`, (err) => {
                if (err) {
                    return res.status(500).send(err);
                }
                // send the player's details to the database
                let query = "INSERT INTO `items` (description, image) VALUES (?, ?)";
                db.query(query, [description, image_name], (err, result) => {
                    if (err) {
                        return res.status(500).send(err);
                    }
                    res.redirect('/');
                });
            });
        } else {
            message = "Invalid File format. Only 'gif', 'jpeg' and 'png' images are allowed.";
            res.render('add-item.html', {
                message,
                title: 'Add a new item'
            });
        }
    },
    editItemPage: (req, res) => {
        const logger = getLogger(basename(__filename));
        let id = req.params.id
        const getAsync = promisify(cache.get).bind(cache);
        const setAsync = promisify(cache.set).bind(cache);

        getAsync(id).then(console.log).catch(console.error);
        let query = "SELECT * FROM `items` WHERE id = ?";
        db.query(query, [id], (err, result) => {
            if (err) {
                return res.status(500).send(err);
            }
            res.render('edit-item.html', {
                title: 'Edit Item',
                item: result[0],
                message: ''
            });
            setAsync(id, JSON.stringify(result[0])).then(console.log).catch(console.error);
        });
    },
    editItem: (req, res) => {
        let id = req.params.id;
        let description = req.body.description;

        let query = "UPDATE `items` SET `description` = ? WHERE `items`.`id` = ?";
        db.query(query, [description, id], (err, result) => {
            if (err) {
                return res.status(500).send(err);
            }
            res.redirect('/');
        });
    },
    deleteItem: (req, res) => {
        const logger = getLogger(basename(__filename));
        let id = req.params.id;
        let getImageQuery = 'SELECT `image` from `items` WHERE `id` = ?';
        let deleteUserQuery = 'DELETE FROM `items` WHERE `id` = ?';

        db.query(getImageQuery, [id], (err, result) => {
            if (err) {
                return res.status(500).send(err);
            }
            db.query(deleteUserQuery, [id], (err, result) => {
                if (err) {
                    return res.status(500).send(err);
                }
                res.redirect('/');
            });
            let image = result[0].image;
            let path = `public/assets/img/${image}`;
            if (existsSync(path)) {
                unlink(`public/assets/img/${image}`, (err) => {
                    if (err) {
                        return res.status(500).send(err);
                    }
                });
            } else {
                logger.warn(`${path}: no such file`);
            }
            return res.status(200)
        });
    }
};