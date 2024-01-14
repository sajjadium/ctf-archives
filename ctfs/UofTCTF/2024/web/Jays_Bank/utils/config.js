const crypto = require("crypto");

const JWT_SECRET =
  process.env.JWT_SECRET || crypto.randomBytes(64).toString("hex");

const FLAG = process.env.FLAG || "uoftctf{fake_flag}";

module.exports = {
  JWT_SECRET,
  FLAG,
};
