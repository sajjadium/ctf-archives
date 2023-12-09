const express = require("express");
const router = express.Router();
const { v4: uuid } = require("uuid");

const { requireAuth } = require("../middlewares/auth");
const { isUuid, validate } = require("../utils/validation");

const db = require("../db");
const { body } = require("express-validator");
const {
  getGenerator,
  fromHex,
  toHex,
  xor,
  getPublicKeyFromPrivateKey,
  verifyToken,
} = require("../utils/numbers");

router.use(requireAuth);

router.get("/:id", async (req, res) => {
  const accountID = parseInt(req.params.id);
  if (
    isNaN(accountID) ||
    (+req.session.user.id !== accountID &&
      req.session.user.username !== process.env.ADMIN_USERNAME)
  ) {
    res.redirect(`/account/${req.session.user.id}`);
    return;
  }

  const user = await db.fetchUserById(accountID);
  if (user == null) {
    res.redirect(`/account/${req.session.user.id}`);
    return;
  }

  if (!user.curve_private_key || !user.session_key) {
    res.render("account", { user });
    return;
  }
  try {
    if (
      req.cookies.secret &&
      /^[0-9a-fA-F]+$/.test(req.cookies.secret) &&
      req.cookies.secret.length === 64
    ) {
      private_key = xor(fromHex(req.cookies.secret), fromHex(user.session_key));
    } else {
      // Regenerate secret
      private_key = fromHex(user.curve_private_key);
      session_key = fromHex(user.session_key);
      encrypted_secret_key = xor(private_key, session_key);
      res.cookie("secret", toHex(encrypted_secret_key));
    }

    const public_key = await getPublicKeyFromPrivateKey(toHex(private_key));
    const generator = await getGenerator();
    const challenge = req.session.user.challenge;

    res.render("account", {
      user: user,
      public_key: public_key,
      generator: generator,
      challenge: challenge,
    });
  } catch (error) {
    console.log({ error });
    res.render("error", {
      message: `Something went wrong`,
    });
  }
});

router.post(
  "/:id/motto",
  body("motto").notEmpty().isString(),
  async (req, res) => {
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const motto = data.motto;
    const accountID = parseInt(req.params.id);
    if (isNaN(accountID) || +req.session.user.id !== accountID) {
      res.redirect(`/account/${req.session.user.id}`);
      return;
    }

    const result = await db.changeMotto(accountID, motto);
    if (result) {
      res.json({
        result: "success",
        redirect: `/account/${accountID}`,
      });
      return;
    }
    res.status(403).json({
      result: "failure",
    });
  }
);

router.post(
  "/:id/token",
  body("token").notEmpty().isString(),
  async (req, res) => {
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const accountID = parseInt(req.params.id);
    if (
      isNaN(accountID) ||
      +req.session.user.id !== accountID ||
      req.session.user.username === process.env.ADMIN_USERNAME
    ) {
      res.redirect(`/account/${req.session.user.id}`);
      return;
    }

    try {
      const user = req.session.user;
      const private_key = user.curve_private_key;
      const challenge = user.challenge;
      const token = fromHex(data.token);

      if (await verifyToken(challenge, private_key, token)) {
        coupon = uuid();
        const result = await db.resetUser(user.id, coupon);

        // Log out the user
        req.session.destroy();

        if (result) {
          res.json({
            result: "success",
            redirect: `/auth/login`,
            coupon: coupon,
          });
          return;
        }
      }
      res.status(403).json({
        result: "failure",
      });
    } catch (error) {
      console.log(error);
      res.render("error", {
        message: `Invalid token for username: ${req.session.user.username}`,
        error,
      });
    }
  }
);

router.post(
  "/:id/coupon",
  body("coupon").notEmpty().isString(),
  async (req, res) => {
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const accountID = parseInt(req.params.id);
    if (
      isNaN(accountID) ||
      +req.session.user.id !== accountID ||
      req.session.user.username === process.env.ADMIN_USERNAME
    ) {
      res.redirect(`/account/${req.session.user.id}`);
      return;
    }

    const requested_coupon = data.coupon;
    if (!isUuid(requested_coupon)) {
      res.status(403).json({
        result: "failure",
        message: "Invalid coupon",
      });
      return;
    }
    const { coupon } = await db.fetchUserById(req.session.user.id);
    try {
      if (requested_coupon === coupon) {
        await db.applyCoupon(req.session.user.id);
        res.json({
          result: "success",
          redirect: `/account/${req.session.user.id}`,
        });
        res.end();
        return;
      }
    } catch (error) {
      console.log(error);
    }
    res.status(403).json({
      result: "failure",
      message: "Invalid coupon",
    });
  }
);

module.exports = router;
