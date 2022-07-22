const crypto = require("crypto");

const db = require("./db.js");

const KEY = crypto.randomBytes(32);

const encrypt = (data) => {
  const iv = Buffer.from(crypto.randomBytes(16));
  const cipher = crypto.createCipheriv('aes-256-gcm', KEY, iv);
  let enc = cipher.update(data, 'utf8', 'base64');
  enc += cipher.final('base64');
  return [enc, iv.toString('base64'), cipher.getAuthTag().toString('base64')].join(".");
};

const decrypt = (data) => {
  try {
    const [enc, iv, authTag] = data.split(".").map(d => Buffer.from(d, 'base64'));
    const decipher = crypto.createDecipheriv('aes-256-gcm', KEY, iv);
    decipher.setAuthTag(authTag);
    let dec = decipher.update(enc, 'base64', 'utf8');
    return dec;
  }
  catch(err) {
    return null;
  }
};

const getUser = (req) => {
  const session = req.cookies.session;
  if(!session) {
    throw new Error("You are not logged in")
  }

  const username = decrypt(session);
  if(!username) {
    throw new Error("You are not logged in");
  }
  
  let user = db.getUser(username);
  if(!user) {
    throw new Error("You are not logged in")
  }

  return user;
};

const setUser = (res, username) => {
  res.cookie("session", encrypt(username));
};

module.exports = { getUser, setUser };