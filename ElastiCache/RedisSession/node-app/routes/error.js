module.exports = {
    getErrorPage: (req, res) => {
        res.render('error.html', {
            title: 'Error',
            error_message: 'Error. Look at the logs for more details.'
        });
    }
};