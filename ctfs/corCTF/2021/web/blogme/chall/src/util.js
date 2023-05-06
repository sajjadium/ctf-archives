const requiresLogin = (req, res, next) => {
    if(req.user)  {
        return next();
    }
    res.redirect("/api/login?error=" + encodeURIComponent(`You must login to complete this action`));
};

module.exports = { requiresLogin };