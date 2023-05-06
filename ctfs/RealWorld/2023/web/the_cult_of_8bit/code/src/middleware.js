const requiresLogin = (req, res, next) => {
    if (!req.user) {
        return res.redirect("/?msg=Login required");
    }
    next();
};

const requiresNoLogin = (req, res, next) => {
    if (req.user) {
        return res.redirect("/?msg=You are already logged in!");
    }
    next();
};

const csrfProtection = (req, res, next) => {
    let token = req.body._csrf || req.query._csrf;
    if (!req.session.hasCSRF || req.csrfToken !== token) {
        return res.redirect("/?msg=Invalid CSRF token");
    }
    next();
};

module.exports = { requiresLogin, requiresNoLogin, csrfProtection };