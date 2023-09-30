function validateReply(req, res, next) {
    var regExp = /[a-zA-Z]/g;
    if (!req.query.reply || regExp.test(req.query.reply) || req.query.reply == "") {
        return res.redirect('/joi');
    }
    next();
}

module.exports = {
    validateReply
}