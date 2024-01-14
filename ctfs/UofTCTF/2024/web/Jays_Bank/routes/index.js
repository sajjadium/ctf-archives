const express = require("express");
const router = express.Router();
const jwtAuth = require("../middleware/authMiddleware.js");
const jwt = require("jsonwebtoken");
const crypto = require("crypto");

const { JWT_SECRET, FLAG } = require("../utils/config.js");

let db;

router.get("/", (req, res) =>
  res.render("index", {
    username: req.user,
  })
);
router.get("/login", (req, res) => {
  res.clearCookie("auth_token");
  res.render("login");
});

router.get("/register", (req, res) => {
  res.render("register");
});

router.post("/login", async (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res
      .status(400)
      .json({ success: false, message: "Missing username or password" });
  }
  if (typeof username !== "string" || typeof password !== "string") {
    return res
      .status(400)
      .json({ success: false, message: "Invalid username or password" });
  }
  const result = await db.login(username, password);
  if (!result) {
    return res
      .status(401)
      .json({ success: false, message: "Invalid username or password" });
  }
  const token = jwt.sign({ username: username }, JWT_SECRET);
  res.cookie("auth_token", token, { httpOnly: true });
  res.json({ success: true, message: "Login successful!" });
});

router.post("/register", async (req, res) => {
  const { username, password } = req.body;

  // Check if username or password is missing
  if (!username || !password) {
    return res
      .status(400)
      .json({ success: false, message: "Missing username or password" });
  }

  // Check if username and password are strings
  if (typeof username !== "string" || typeof password !== "string") {
    return res
      .status(400)
      .json({ success: false, message: "Invalid username or password" });
  }

  // Check username length
  if (username.length < 10) {
    return res
      .status(400)
      .json({ success: false, message: "Username must be at least 10 characters long" });
  }

  // Check password length and complexity
  const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{10,}$/;
  if (!passwordRegex.test(password)) {
    return res
      .status(400)
      .json({ success: false, message: "Password must be at least 10 characters long and include at least one digit, one special character, one uppercase letter, and one lowercase letter" });
  }

  // Check if username already exists
  if (await db.userExists(username)) {
    return res
      .status(400)
      .json({ success: false, message: "Username already exists" });
  }

  // Proceed with registration
  await db.register(username, password, db.convert({ role: "user" }));
  res.json({ success: true, message: "Registration successful!" });
});


router.get("/dashboard", jwtAuth, async (req, res) => {
  let username = req.user.username;

  let data = await db.getData(username);
  try {
    data = JSON.parse(data);
  } catch {
    return res.status(302).redirect("/profile");
  }
  if (
    !data.phone ||
    !data.credit_card ||
    !data.secret_question ||
    !data.secret_answer
  ) {
    return res.status(302).redirect("/profile");
  }

  res.render("dashboard", {
    username: username,
    phone: data.phone,
    credit_card: data.credit_card,
    flag: data.role === "admin" ? FLAG : null,
  });
});

router.get("/profile", jwtAuth, async (req, res) => {
  let username = req.user.username;
  let data = await db.getData(username);
  console.log(data)

  try {
    data = JSON.parse(data);
  } catch {
    return res.render("profile", {
      incomplete: true,
      username: username,
      phone: null,
      credit_card: null,
      secret_question: null,
    });
  }

  if (
    !data.phone ||
    !data.credit_card ||
    !data.secret_question ||
    !data.secret_answer
  ) {
    return res.render("profile", {
      incomplete: true,
      username: username,
      phone: null,
      credit_card: null,
      secret_question: null,
    });
  }

  res.render("profile", {
    incomplete: false,
    username: username,
    phone: data.phone,
    credit_card: data.credit_card,
    secret_question: data.secret_question,
  });
});

router.put("/profile", jwtAuth, async (req, res) => {
  let username = req.user.username;

  let existingData = await db.getData(username);
  try {
    existingData = JSON.parse(existingData);
  } catch {
    existingData = { role: "user" };
  }

  let { phone, credit_card, secret_question, secret_answer, current_password } =
    req.body;

  if (!current_password) {
    return res.status(400).json({
      success: false,
      message: "Missing current password",
    });
  }

  if (
    !(
      typeof current_password === "string" &&
      (await db.verifyPassword(username, current_password))
    )
  ) {
    return res
      .status(401)
      .json({ success: false, message: "Invalid current password" });
  }

  if (!phone || !credit_card || !secret_question || !secret_answer) {
    return res.status(400).json({ success: false, message: "Missing fields" });
  }

  if (phone.length !== 10 || isNaN(phone)) {
    return res
      .status(400)
      .json({ success: false, message: "Invalid phone number" });
  }

  if (credit_card.length !== 16 || isNaN(credit_card)) {
    return res
      .status(400)
      .json({ success: false, message: "Invalid credit card number" });
  }

  if (typeof secret_question !== "string" || secret_question.length > 45) {
    return res
      .status(400)
      .json({ success: false, message: "Invalid secret question" });
  }

  if (typeof secret_answer !== "string" || secret_answer.length > 45) {
    return res
      .status(400)
      .json({ success: false, message: "Invalid secret answer" });
  }

  try {
    await db.updateData(
      username,
      db.convert({
        phone,
        credit_card,
        secret_question,
        secret_answer,
        role: "user",
      })
    );

    return res
      .status(200)
      .json({ success: true, message: "Successfully updated" });
  } catch {
    return res
      .status(400)
      .json({ success: false, message: "Failed to update DB" });
  }
});

router.put("/change_password", jwtAuth, async (req, res) => {
  let username = req.user.username;

  let data = await db.getData(username);
  try {
    data = JSON.parse(data);
  } catch {
    data = { role: "user" };
  }
  if (!data.secret_question || !data.secret_answer) {
    return res.status(400).json({
      success: false,
      message:
        "You need to set a secret question + answer before you can change your password",
    });
  }

  const { secret_answer } = req.body;

  if (
    typeof secret_answer !== "string" ||
    secret_answer.toLowerCase() !== data.secret_answer
  ) {
    return res
      .status(400)
      .json({ success: false, message: "Incorrect secret answer" });
  }

  if (typeof req.body.new_password !== "string") {
    return res
      .status(400)
      .json({ success: false, message: "Invalid password" });
  }

  await db.changePassword(username, req.body.new_password);

  return res
    .status(200)
    .json({ success: true, message: "Successfully changed password" });
});

router.get("/logout", jwtAuth, (req, res) => {
  res.clearCookie("auth_token");
  res.status(302).redirect("/");
});

module.exports = (database) => {
  db = database;
  return router;
};
