import verifyUser from "@/server/middleware/verifyUser";
import connectDb from "@/server/middleware/mongoose";
import cookie from "cookie";
import cors from "@/server/middleware/cors";

const handler = async (req, res) => {
  const cookies = req.headers?.cookies || req.cookies;
  const token = cookies["token"];

  if (token) {
    res.setHeader(
      "Set-Cookie",
      cookie.serialize("token", token, {
        httpOnly: true,
        secure: process.env.NODE_ENV !== "development",
        maxAge: -1,
        sameSite: "strict",
        path: "/",
        domain:
          process.env.NODE_ENV === "development"
            ? "localhost"
            : "",
      })
    );

    res.status(200).json({ isLoggedIn: false, data: null });
  } else {
    res.status(200).json({ isLoggedIn: false, data: null });
  }
};

export default cors(verifyUser(connectDb(handler)));
