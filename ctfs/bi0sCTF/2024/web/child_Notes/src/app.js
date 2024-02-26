const express = require("express");
const crypto = require("crypto");
const uuid = require("uuid");
const User = require("./models/User");
const Post = require("./models/Post");

const visit = require("./bot").visit;

const admin_pass = crypto.randomBytes(16).toString("hex");

const { init } = require("./utils");

const PORT = 8000;

const app = express();

function loggedIn(req, res, next) {
  if (req.session && req.session.username) {
    next();
  } else {
    res.redirect("/login");
  }
}

function adminOnly(req, res, next) {
  if (req.session && req.session.username && req.session.username === "admin") {
    next();
  } else {
    res.status(403).send("Forbidden");
  }
}

function check(rawQuery) {
  return /^[a-zA-Z0-9\&\=\[\]\_]+$/.test(rawQuery);
}

function checkContent(content) {
  return typeof content === "string" && !/meta|svg|math/gi.test(content);
}

function validUser(username) {
  return (
    typeof username === "string" &&
    /^[a-z-A-Z-0-9-\.-\/]+$/.test(username) &&
    username.length <= 50
  );
}

const session = require("express-session");

app.use(express.static("./public"));

app.use(
  session({
    cookie: {
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24 * 7,
    },
    resave: false,
    saveUninitialized: true,
    secret: crypto.randomBytes(32).toString("hex"),
  })
);
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString("hex");
  res.setHeader(
    "Content-Security-Policy",
    `
        default-src 'self';
        script-src 'nonce-${res.locals.nonce}' 'unsafe-inline';
        object-src 'none';
        base-uri 'none';
        connect-src 'self';
        navigate-to 'self';
    `
      .trim()
      .replace(/\s+/g, " ")
  );

  res.setHeader("Cache-Control", "no-cache,no-store");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
  res.setHeader("Cross-Origin-Resource-Policy", "same-origin");
  res.setHeader("Document-Policy", "force-load-at-top");
  //TODO: Add more headers
  next();
});

app.use(express.urlencoded({ extended: false }));
app.set("view engine", "hbs");

app.get("/", loggedIn, (req, res) => {
  return res.render("index", (data = { username: req.session.username }));
});

app.get("/login", (req, res) => {
  return res.render("login");
});

app.post("/login", async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  if (username && password && validUser(username)) {
    try {
      const user = await User.query().findOne({ username, password });

      if (!user) {
        return res.render("login", {
          error: "Username or password is not correct",
        });
      }

      req.session.username = username;
      console.log(`${req.url} Log: ${req.session.username} logged in`);
      return res.redirect("/");
    } catch (err) {
      console.log(err);
      return res.render("login", { error: "Invalid username or password" });
    }
  } else {
    console.log(`${req.url} Error: invalid username or password`);
    return res.render("login", { error: "Invalid username or password" });
  }
});

app.post("/register", async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  if (
    username &&
    password &&
    validUser(username) &&
    !username.includes("admin")
  ) {
    try {
      const existingUser = await User.query().findOne({ username });

      if (existingUser !== undefined) {
        return res.render("login", { error: "Username already exists" });
      }

      await User.query().insert({
        username: username,
        password: password,
      });

      req.session.username = username;
      console.log(`${req.url} Log: ${req.session.username} registered`);
      return res.redirect("/");
    } catch (err) {
      console.log(err);
      return res.render("login", { error: "Invalid username or password" });
    }
  } else {
    return res.render("login", { error: "Invalid username or password" });
  }
});

app.post("/create", loggedIn, async (req, res) => {
  const title = req.body.title;
  const content = req.body.content;
  const author = req.session.username;
  const uid = uuid.v4();

  if (title && typeof title === "string" && content && checkContent(content)) {
    try {
      await Post.query().insert({
        id: uid,
        title: title,
        content: content,
        author: author,
      });

      return res.redirect("/post/" + uid + "/");
    } catch (err) {
      console.log(err);
      return res.render("index", { error: "Invalid title or content" });
    }
  } else {
    return res.render("index", { error: "Invalid title or content" });
  }
});

app.get("/posts", loggedIn, async (req, res) => {
  try {
    const posts = await Post.query().where("author", req.session.username);

    return res.render("posts", { rows: posts });
  } catch (err) {
    console.log("/posts Error:", err);
    return res.render("posts", { error: "Invalid request" });
  }
});

app.get("/post/:id", loggedIn, async (req, res) => {
  try {
    const post = await Post.query().findOne({
      id: req.params.id,
      author: req.session.username,
    });

    if (post) {
      return res.render("post", post);
    } else {
      return res.render("post", { error: "Invalid post id" });
    }
  } catch (err) {
    console.log("/post/:id Error:", err);
    return res.render("post", { error: "Invalid post id" });
  }
});

app.get("/search", loggedIn, async (req, res) => {
  if (!check(req.url.slice(req.url.indexOf("?") + 1))) {
    console.log("/search Error: Invalid search query");
    return res.json({ error: "Invalid search query" });
  }

  const query = req.query.q || "";
  const filter = req.query.f || "*";

  try {
    const posts = await Post.query()
      .column(filter)
      .where("title", "LIKE", `%${query}%`)
      .andWhere("author", req.session.username);

    return res.render("search", { posts: posts });
  } catch (err) {
    console.log("/search Error:", err);
    return res.json({ error: "Invalid search query" });
  }
});

app.get("/logout", (req, res) => {
  if (req.session.username) delete req.session.username;
  res.redirect("/login");
});

app.post("/verify", loggedIn, async (req, res) => {
  let uid = req.body.id.toString();
  let user = req.session.username;
  await visit(uid, user, admin_pass);
  return res.json({ status: "ok" });
});

//Just for admin

app.post("/delete", adminOnly, async (req, res) => {
  try {
    await Post.query().delete().where({
      id: req.body.id,
    });

    return res.json({ success: "Post deleted" });
  } catch (err) {
    console.log("/delete Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/all", adminOnly, async (req, res) => {
  try {
    const page = +req.query.page || 1;
    const limit = +req.query.limit || 100;
    const start = (page - 1) * limit;

    const posts = Post.query().offset(start).limit(limit);
    const users = User.query().offset(start).limit(limit);

    return res.json([posts, users]);
  } catch (err) {
    console.log("/all Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/verify", adminOnly, async (req, res) => {
  try {
    const uid = req.query.uid.toString();
    const user = req.query.user.toString();

    const post = await Post.query().findOne({ id: uid });

    if (!post) {
      console.log("/verify Error: Invalid id");
      return res.json({ error: "Invalid id" });
    }

    return res.render("verify", { ...post, user: user });
  } catch (err) {
    console.log("/verify Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
});

app.get("/:username/block", adminOnly, async (req, res) => {
  try {
    if (req.query.block === "true" && req.params.username !== "admin") {
      await User.query().delete().where({ username: req.params.username });

      return res.json({ success: "User blocked" });
    } else {
      return res.json({ error: "Invalid query" });
    }
  } catch (err) {
    console.log("/:username/block Error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
});

(async function () {
  await init(admin_pass);
  app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
  });
})();
