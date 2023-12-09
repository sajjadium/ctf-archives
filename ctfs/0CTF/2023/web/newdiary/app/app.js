const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const { assert } = require("console");
const { sha256, random_bytes } = require("./utils");
const { visit } = require("./bot");
const crypto = require("crypto");
const genNonce = () =>
  "_"
    .repeat(32)
    .replace(/_/g, () =>
      "abcdefghijklmnopqrstuvwxyz0123456789".charAt(crypto.randomInt(36))
    );
const report = new Map();
const now = () => {
  return Math.floor(+new Date() / 1000);
};

const app = express();

app.use("/static", express.static("static"));

app.use(bodyParser.urlencoded({ extended: false }));
app.use(
  session({
    cookie: { maxAge: 600000 },
    secret: random_bytes(64),
  })
);

app.use((req, res, next) => {
  res.nonce = genNonce();
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Cache-Control", "no-cache, no-store");
  next();
});

app.engine("html", require("ejs").renderFile);
app.set("view engine", "html");

const users = new Map([[]]);

const notes = new Map([[]]);

const share_notes = new Map([[]]);

app.all("/", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/login");
  } else {
    return res.render("index", {
      username: req.session.username,
      notes: notes.get(req.session.username) || [],
    });
  }
});

app.get("/login", (req, res) => {
  if (req.session.username) {
    return res.redirect("/");
  }
  return res.render("login");
});

app.post("/login", (req, res) => {
  if (req.session.username) {
    return res.redirect("/");
  }
  const { username, password } = req.body;

  if (
    username.length < 4 ||
    username.length > 10 ||
    typeof username !== "string" ||
    password.length < 6 ||
    typeof password !== "string"
  ) {
    return res.render("login", { msg: "invalid data" });
  }

  if (users.has(username)) {
    if (users.get(username) === sha256(password)) {
      req.session.username = username;

      return res.redirect("/");
    } else {
      return res.render("login", { msg: "Invalid Password" });
    }
  } else {
    users.set(username, sha256(password));
    req.session.username = username;

    return res.redirect("/");
  }
});

app.post("/write", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/");
  }
  const username = req.session.username;
  const { title, content } = req.body;

  assert(title && typeof title === "string" && title.length < 30);
  assert(content && typeof content === "string" && content.length < 256);

  const user_notes = notes.get(username) || [];
  user_notes.push({
    title,
    content,
    username,
  });
  notes.set(req.session.username, user_notes);

  return res.redirect("/");
});

app.get("/read", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/");
  }

  return res.render("read", { nonce: res.nonce });
});

app.get("/read/:id", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/");
  }

  const { id } = req.params;
  if (!/^\d+$/.test(id)) {
    return res.json({ status: 401, message: "Invalid parameter" });
  }

  const user_notes = notes.get(req.session.username);
  const found = user_notes && user_notes[id];

  if (found) {
    return res.json({ title: found.title, content: found.content });
  } else {
    return res.json({ title: "404 not found", content: "no such note" });
  }
});

app.get("/share_diary/:id", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/");
  }
  const tmp = share_notes.get(req.session.username) || [];
  const { id } = req.params;

  if (!/^\d+$/.test(id)) {
    return res.json({ status: 401, message: "Invalid parameter" });
  }

  const user_notes = notes.get(req.session.username);
  const found = user_notes && user_notes[id];
  if (found) {
    tmp.push(found);
    share_notes.set(req.session.username, tmp);
    return res.redirect("/share");
  } else {
    return res.json({ title: "404 not found", content: "no such note" });
  }
});

app.all("/share", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/login");
  } else {
    return res.render("share", {
      notes: share_notes.get(req.session.username) || [],
    });
  }
});

app.get("/share/read", (req, res) => {
  return res.render("read_share", { nonce: res.nonce });
});

app.get("/share/read/:id", (req, res) => {
  const { id } = req.params;
  const username = req.query.username;

  let found;
  if (!/^\d+$/.test(id)) {
    return res.json({ status: 401, message: "Invalid parameter" });
  }
  try {
    if (username !== undefined) {
      found = share_notes.get(username);
      if (found) {
        return res.json({
          title: found[id].title,
          content: found[id].content,
          username: found[id].username,
        });
      }
    } else if (req.session.username) {
      found = share_notes.get(req.session.username);
      if (found) {
        return res.json({
          title: found[id].title,
          content: found[id].content,
          username: found[id].username,
        });
      }
    }
  } catch {
    return res.json({ title: "404 not found", content: "no such note" });
  }
  return res.json({ title: "404 not found", content: "no such note" });
});

app.all("/logout", (req, res) => {
  req.session.destroy();
  return res.redirect("/");
});

app.get("/report", (req, res) => {
  if (!req.session.username) {
    return res.redirect("/login");
  }
  const id = req.query.id;
  const username = req.query.username;
  if (typeof id === "string" && /^\d+$/.test(id)) {
    try {
      if (
        report.has(req.session.username) &&
        report.get(req.session.username) + 30 > now()
      ) {
        return res.json({ error: "too fast" });
      }
      report.set(req.session.username, now());
      visit(id, username);
      return res.json({ msg: "visited" });
    } catch (e) {
      return res.status(500).json({ error: "failed" });
    }
  }
  res.status(400).json({ error: "bad url" });
});

app.listen(80);
console.log("Server running on 80....");
