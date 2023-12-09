const express = require("express");
const router = express.Router();
const { body } = require("express-validator");
const { validate } = require("../utils/validation");
const bcrypt = require("bcryptjs");
const { v4: uuid } = require("uuid");
const db = require("../db");
const { requireAuth, requireAPIKey } = require("../middlewares/auth");
const {
  fromHex,
  toHex,
  getPrivateKey,
  getSessionKey,
  xor,
  genChallenge,
} = require("../utils/numbers");

router.get("/login", (req, res) => {
  res.render("login", {
    message: "",
  });
});

router.get("/register", (req, res) => {
  res.render("register", {
    message: "Registrations are currently closed",
  });
});

// TODO: Flash user with its coupon
router.post(
  "/login",
  body("username").notEmpty().isString(),
  body("password").notEmpty().isString(),
  async (req, res) => {
    // This function is not part of the challenge
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const user = await db.fetchUser(data.username);
    if (
      user &&
      user.enabled &&
      bcrypt.compareSync(data.password, user.password)
    ) {
      if (user.curve_private_key && user.session_key) {
        // Generate public key and challenge
        encrypted_secret_key = xor(
          fromHex(user.curve_private_key),
          fromHex(user.session_key)
        );
        res.cookie("secret", toHex(encrypted_secret_key));
        user.challenge = genChallenge();
      }

      req.session.user = user;
      res.json({
        result: "success",
        redirect: "/",
      });
    } else {
      req.session.destroy();
      res.status(401).json({
        result: "failure",
        message: "Authentication failed",
      });
    }
  }
);

router.post(
  "/register",
  requireAPIKey,
  body("username").notEmpty().isString(),
  body("password").notEmpty().isString(),
  async (req, res) => {
    // This function is not part of the challenge
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const password_enc = bcrypt.hashSync(data.password, 10);
    coupon = uuid();
    private_key = toHex(await getPrivateKey());
    session_key = toHex(getSessionKey(+process.env.KEY_LENGTH));

    db.addUser(
      data.username,
      password_enc,
      private_key,
      session_key,
      coupon
    ).then((success) => {
      if (success) {
        res.json({
          result: "success",
        });
      } else {
        res.status(400).json({
          result: "failure",
        });
      }
    });
  }
);

router.patch(
  "/register",
  requireAPIKey,
  body("username").notEmpty().isString(),
  body("password"),
  body("new_username"),
  body("enabled").notEmpty().isBoolean(),
  (req, res) => {
    // This function is not part of the challenge
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const maybe_password_enc = data.password
      ? bcrypt.hashSync(data.password, 10)
      : data.password;

    if (data.enabled === false || data.new_username) {
      req.sessionStore.all((err, sessions) => {
        if (err) {
          console.error(err);
        } else {
          const sessionNames = Object.keys(sessions);

          const userSessions = sessionNames.filter(
            (s) =>
              sessions[s].user && sessions[s].user.username === data.username
          );

          userSessions.forEach((s) =>
            req.sessionStore.destroy(s, (err) => {
              if (err) console.error(err);
            })
          );
        }
      });
    }

    db.updateUser(
      data.username,
      maybe_password_enc,
      data.new_username,
      data.enabled
    ).then((success) => {
      if (success) {
        res.json({
          result: "success",
        });
      } else {
        res.status(400).json({
          result: "failure",
        });
      }
    });
  }
);

router.get("/logout", requireAuth, (req, res) => {
  req.session.destroy();
  res.redirect("/auth/login");
});

module.exports = router;
