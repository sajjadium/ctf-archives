const crypto = require("crypto");

const app = db.getSiblingDB('app');
app.users.insertOne({ user: crypto.randomBytes(8).toString("hex"), pass: crypto.randomBytes(64).toString("hex") });

const secret = db.getSiblingDB('secret');
secret.flag.insertOne({ flag: process.env.FLAG || "dice{test_flag}" });
