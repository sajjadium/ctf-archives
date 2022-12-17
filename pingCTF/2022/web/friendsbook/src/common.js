import crypto from "crypto";
export const SECRET = crypto.randomBytes(128).toString("hex");
