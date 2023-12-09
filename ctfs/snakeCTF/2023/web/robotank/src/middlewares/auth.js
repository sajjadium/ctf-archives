module.exports = {
  requireAuth: (req, res, next) => {
    if (req.session && req.session.user) {
      return next();
    } else {
      res.redirect("/auth/login");
    }
  },
  requireAdmin: (req, res, next) => {
    if (req.session.user.username === process.env.ADMIN_USERNAME) {
      return next();
    } else {
      res.redirect("/");
    }
  },
  requireAPIKey: (req, res, next) => {
    // This function is not part of the challenge
    if (
      req.headers["x-api-key"] &&
      req.headers["x-api-key"] === process.env.REGISTER_API_KEY
    ) {
      return next();
    } else {
      res.redirect("/");
    }
  },
};
