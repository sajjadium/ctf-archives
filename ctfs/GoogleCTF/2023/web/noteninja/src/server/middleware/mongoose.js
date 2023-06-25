import mongoose from "mongoose";
import CryptoJS from "crypto-js";
import User from "../models/User";

const connectDb = (handler) => async (req, res) => {
  if (mongoose.connections[0].readyState) {
    return handler(req, res);
  }

  mongoose.set("strictQuery", false);
  mongoose.connect(process.env.MONGO_URL);

  try {
    const adminUser = await User.findOne({ email: process.env.ADMIN_EMAIL })
    if (!adminUser) {
      let u = new User({
        name: process.env.ADMIN_NAME,
        email: process.env.ADMIN_EMAIL,
        password: CryptoJS.AES.encrypt(
          process.env.ADMIN_PASS,
          process.env.SECRET_KEY
        ).toString(),
      });
      await u.save();
    }
  } catch (error) {
    console.log("admin creation failed: " + error);
  }
  return handler(req, res);
};

export default connectDb;
