const express = require("express");
const crypto = require("crypto");
const fs = require("fs");

const app = express();
app.use(express.json());

const SECRET = crypto.randomBytes(32).toString("hex");
const FLAG = fs.readFileSync("/flag.txt", "utf8").trim();

function expectedToken(user) {
  return crypto.createHmac("sha256", SECRET).update(user).digest("hex");
}

app.post("/login", (req, res) => {
  const { user, token } = req.body || {};

  if (user !== "admin") {
    return res.status(403).json({ error: "unknown user" });
  }

  const expected = expectedToken(user);

  const tokens = [].concat(token);
  if (!tokens.every((candidate) => candidate === expected)) {
    return res.status(403).json({ error: "bad token" });
  }

  return res.json({ flag: FLAG });
});

app.get("/", (req, res) => res.sendStatus(200));

const PORT = process.env.PORT || 3000;
app.listen(PORT, "0.0.0.0", () => console.log("listening on " + PORT));
