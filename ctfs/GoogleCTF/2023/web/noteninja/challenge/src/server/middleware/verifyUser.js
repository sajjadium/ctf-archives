const jwt = require("jsonwebtoken");
const JWT_SECRET = process.env.JWT_SECRET;

const verifyUser = (handler, action) => {
  return async (req, res) => {
    const cookies = req.headers?.cookies || req.cookies;
    const user = cookies["token"];

    if (!user) {
      res.status(400).json({
        hasError: true,
        message:
          "You are not logged in. Please login first to access your account.",
      });
    } else {
      try {
        const data = jwt.verify(user, JWT_SECRET);
        req.id = data.id;
        req.user = data;

        if (data) {
          return handler(req, res);
        } else {
          res.status(401).json({
            hasError: true,
            message: "Token Expired! Please login again.",
          });
        }
      }
      catch (err) {
        res.status(500).json({ isLoggedIn: false, data: null, msg: err.message })
      }
    }
  };
};

export default verifyUser;
