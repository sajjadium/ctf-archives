const authenticationMiddleware = (req, res, next) => {
    if (req.originalUrl === '/login' || req.originalUrl === '/register') {
        return next();
    }

    if (req.session.userId) {
        return next();
    }
    return res.redirect('/login');
}

module.exports = authenticationMiddleware;