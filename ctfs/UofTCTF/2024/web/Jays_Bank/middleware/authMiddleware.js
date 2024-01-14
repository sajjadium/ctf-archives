const jwt = require("jsonwebtoken");
const {JWT_SECRET} = require("../utils/config.js");

const jwtAuth = (req, res, next) => {
  const token = req.cookies.auth_token;
  if (!token) {
    return res.status(401).redirect("/login");
  }
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    if (typeof decoded !== "object" || typeof decoded.username !== "string") {
      return res.status(401).redirect("/login");
    }
    req.user = { username: decoded.username };
    next();
  } catch  {
    res.status(401).redirect("/login");
  }
};

module.exports = jwtAuth;
