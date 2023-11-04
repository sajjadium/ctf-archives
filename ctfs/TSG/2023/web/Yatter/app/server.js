const express = require("express");
const session = require("express-session");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const User = require("./models/User.js");
const Post = require("./models/Post.js");

process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection at:", promise, "reason:", reason);
});

mongoose.connect(process.env.MONGO_URL);

const app = express();
const port = parseInt(process.env.PORT ?? "8080", 10);

app.set("view engine", "ejs");

app.use(express.urlencoded({ extended: true }));

app.use(session({
  secret: "your-secret-key",
  resave: false,
  saveUninitialized: true,
}));

app.get("/", async (req, res) => {
  const posts = await Post.find()
    .populate("author")
    .exec();

  const userId = req.session.userId;
  const me = await User.findById(userId);

  res.render("home", { me, posts });
});

app.get("/register", (req, res) => {
  res.render("register", { error: null });
});

app.post("/register", async (req, res) => {
  const { username, password } = req.body;

  const existingUser = await User.findOne({ username });
  if (existingUser) {
    return res.render("register", { error: "Username is already in use" });
  }

  const salt = await bcrypt.genSalt();
  const hashedPassword = await bcrypt.hash(password, salt);

  const newUser = new User({
    username,
    password: hashedPassword,
  });
  await newUser.save();

  req.session.userId = newUser._id;

  res.redirect("/");
});

app.get("/login", (req, res) => {
  res.render("login", { error: null });
});

app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });

  if (user && (await bcrypt.compare(password, user.password))) {
    req.session.userId = user._id;
    res.redirect("/");
  } else {
    res.render("login", { error: "Invalid username or password" });
  }
});

app.post("/logout", (req, res) => {
  if (req.session) {
    req.session.destroy((err) => {
      if (err) {
        return res.status(500).send("Error");
      }
      res.clearCookie("connect.sid");
      res.redirect("/");
    });
  } else {
    res.send("You are not logged in");
  }
});

app.get("/@:username", async (req, res) => {
  const { username } = req.params;
  const tab = req.query.tab ?? "posts";

  const user = await User.findOne({ username })
    .populate(tab)
    .exec();

  const userId = req.session.userId;
  const me = await User.findById(userId);

  res.render("user", { me, user, tab });
});

app.get("/@:username/:postId", async (req, res) => {
  const { postId } = req.params;

  const post = await Post.findById(postId)
    .populate("author")
    .populate("likes")
    .exec();

  const userId = req.session.userId;
  const me = await User.findById(userId);

  res.render("post", { me, post });
});

app.post("/post", async (req, res) => {
  const userId = req.session.userId;
  if (!userId) {
    return res.status(401).send("You are not logged in");
  }

  const { content } = req.body;

  const newPost = new Post({
    author: userId,
    content,
  });
  await newPost.save();

  res.redirect("back");
});

app.post("/users/:userId/follow", async (req, res) => {
  const userId = req.session.userId;
  if (!userId) {
    return res.status(401).send("You are not logged in");
  }

  const me = await User.findById(userId);

  const followedUserId = req.params.userId;
  const followedUser = await User.findById(followedUserId);

  if (userId === followedUserId) {
    return res.status(401).send("You cannot follow yourself");
  }

  me.following.push(followedUser._id);
  await me.save();

  followedUser.followers.push(me._id);
  await followedUser.save();

  res.redirect("back");
});

app.post("/users/:userId/unfollow", async (req, res) => {
  const userId = req.session.userId;
  if (!userId) {
    return res.status(401).send("You are not logged in");
  }

  const me = await User.findById(userId);

  const followedUserId = req.params.userId;
  const followedUser = await User.findById(followedUserId);

  if (userId === followedUserId) {
    return res.status(401).send("You cannot unfollow yourself");
  }

  me.following = me.following.filter((id) => !id.equals(followedUser._id));
  await me.save();

  followedUser.followers = followedUser.followers.filter((id) =>
    !id.equals(me._id)
  );
  await followedUser.save();

  res.redirect("back");
});

app.post("/posts/:postId/like", async (req, res) => {
  const userId = req.session.userId;
  if (!userId) {
    return res.status(401).send("You are not logged in");
  }

  const me = await User.findById(userId);

  const likedPostId = req.params.postId;
  const likedPost = await Post.findById(likedPostId);

  likedPost.likes.push(me._id);
  await likedPost.save();

  res.redirect("back");
});

app.post("/posts/:postId/unlike", async (req, res) => {
  const userId = req.session.userId;
  if (!userId) {
    return res.status(401).send("You are not logged in");
  }

  const me = await User.findById(userId);

  const likedPostId = req.params.postId;
  const likedPost = await Post.findById(likedPostId);

  likedPost.likes = likedPost.likes.filter((id) => !id.equals(me._id));
  await likedPost.save();

  res.redirect("back");
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
