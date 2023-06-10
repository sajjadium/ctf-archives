const express = require('express');
const cry = require('crypto');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const cookieParser = require('cookie-parser');
const secret = "0ca04547f860592dbb2be76b4da2c73e6cc072e6d874bd127801763be8ea74c1c02a5d6d5d79d0989eaf8f67ff2c7512c4524c20b2e126e53afe68ea9c13884b";
const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.set('view engine', 'ejs');

function auth(req, res, next) {
  token = req.cookies?.token
  if (!token) return res.sendStatus(401);
  jwt.verify(token, secret, (err, data) => {
    if (err) return res.sendStatus(403);
    req.data = data;
    next();
  })
}
app.get("/", (req, res) => { res.sendFile(__dirname + "/views/index.html") });
app.get("/static/bg.jpg", (req, res) => res.sendFile(__dirname + "/static/bg.jpg"));

app.post("/", (req, res) => {
  data = {
    username: req.body.username, tickets: [
      cry.randomBytes(111).toString('hex'),
      cry.randomBytes(111).toString('hex'),
      cry.randomBytes(111).toString('hex'),
      cry.randomBytes(111).toString('hex'),
      cry.randomBytes(111).toString('hex')]
  };
  const token = jwt.sign(data, secret);
  res.cookie('token', token);
  res.redirect("/gamble");
})

app.get("/gamble", auth, (req, res) => {
  const winner = cry.randomBytes(111).toString('hex');
  if (req.data?.tickets?.indexOf(winner) != -1) {
    res.render("gamble.ejs", {msg: `Congrats! The flag is ${fs.readFileSync("flag.txt", "utf8")}.` });
  } else {
    res.render("gamble.ejs", {msg: "Nope. Better luck next time..."});
  }
})

app.listen(port, () => {
  console.log(`App server listening on ${port}. (Go to http://localhost:${port})`);
});
