const crypto = require("crypto");
const express = require("express");
const session = require("express-session");
const _ = require("lodash");

const PORT = process.env.PORT || process.exit(1);

const db = require("./db");
const app = express();

app.use(
  session({
    secret: crypto.randomBytes(32).toString("base64"),
    resave: false,
    saveUninitialized: true,
  })
);

app.set("view engine", "ejs");
app.use(express.urlencoded());

const hasTooLongParams = (params) => {
  return _.some(params, (v) => v.length > 500);
};

app.use((req, _res, next) => {
  if (hasTooLongParams(req.body) || hasTooLongParams(req.query)) {
    throw new Error("<marquee>Too long params</marquee>");
  } else {
    next();
  }
});

app.use((req, res, next) => {
  const nonce = crypto.randomBytes(32).toString("base64");
  res.setHeader(
    "Content-Security-Policy",
    `default-src 'self'; script-src 'nonce-${nonce}'; base-uri 'none';`
  );
  req.nonce = nonce;
  next();
});

app.use("/static", express.static("static"));
app.use("/report", require("./report"));

app.get("/error", (req, res) => {
  res.status(400);
  res.render("error", {
    msg: req.query.msg,
    url: req.query.url,
  });
});

app.get("/login", (req, res) => {
  if (req.session.userId != null) {
    res.redirect("/");
  } else {
    res.render("login");
  }
});

app.post("/login", (req, res) => {
  const user = {
    name: req.body.name,
    password: req.body.password,
  };

  const user2 = db.getUserByName(user);
  if (
    user2 == null ||
    user2.name !== user.name ||
    user2.password !== user.password
  ) {
    throw new Error("<marquee>Login failed</marquee>");
  }

  req.session.userId = user2.id;
  res.redirect("/");
});

app.get("/logout", (req, res) => {
  req.session.destroy();
  res.redirect("/login");
});

app.get("/signup", (req, res) => {
  if (req.session.userId != null) {
    res.redirect("/");
  }
  res.render("signup");
});

app.post("/signup", (req, res) => {
  const user = {
    name: req.body.name,
    password: req.body.password,
  };
  if (user.name == null || user.password == null) {
    throw new Error("<marquee>Username or password not found</marquee>");
  }
  if (user.name.length < 6 || user.password.length < 6) {
    throw new Error("<marquee>Username or password is too short</marquee>");
  }
  const id = db.addUser(user).id;
  req.session.userId = id;

  res.redirect("/");
});

app.use((req, res, next) => {
  if (req.session.userId == null) {
    res.redirect("/login");
  } else {
    next();
  }
});

app.post("/createNote", (req, res) => {
  const note = req.body.note;
  if (note == null) {
    throw new Error("<marquee>Note not found</marquee>");
  }
  const user = db.getUser(req.session.userId);
  db.addNote(user, note);
  res.redirect("/");
});

app.get("/", (req, res) => {
  const user = db.getUser(req.session.userId);
  const notes = db.getNotes(user);
  const query = req.query.search ?? "";
  const filteredNotes = notes.filter((note) => _.includes(note, query));

  res.render("index", {
    query,
    notes,
    filteredNotes,
    nonce: req.nonce,
  });
});

app.use(function (err, req, res, _next) {
  res.redirect(`/error?msg=${err.message}&url=${req.url}`);
});

app.listen(PORT, () => {
  console.log("Started");
});
