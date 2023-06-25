import connectDb from "@/server/middleware/mongoose";
import jwt from "jsonwebtoken";
import cors from "@/server/middleware/cors";

const handler = async (req, res) => {
  const cookies = req.headers?.cookies || req.cookies;
  const user = cookies["token"];

  if (!user) {
    res.status(200).json({
      isLoggedIn: false,
      data: null,
    });
  } else {
    try {
      const data = jwt.verify(user, process.env.JWT_SECRET);

      data
        ? res.status(200).json({ isLoggedIn: true, data: data })
        : res.status(200).json({ isLoggedIn: false, data: null });
      if (!data) {
        res.status(200).json({
          isLoggedIn: false,
          msg: err,
          data: null,
        });
      }
    }
    catch (err) {
      res.status(500).json({ isLoggedIn: false, data: null, msg: err.message })
    }
  }
};

export default cors(connectDb(handler));
