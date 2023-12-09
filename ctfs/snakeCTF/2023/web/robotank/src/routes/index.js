const express = require("express");
const router = express.Router();

const db = require("../db");
const { requireAuth } = require("../middlewares/auth");
const { body } = require("express-validator");
const { validate } = require("../utils/validation");

router.get("/", requireAuth, async (req, res) => {
  let items = await db.fetchItems();
  const has_shield = await db.hasShieldActivated(req.session.user.id);
  items = items.map((x) => {
    let color;
    let disabled;
    switch (x.owner) {
      case req.session.user.id:
        color = "success";
        disabled = false;
        action = `sendAction('${x.name}')`;
        break;
      case null:
      case undefined:
        color = "primary";
        disabled = false;
        action = `buyAction('${x.name}')`;
        break;

      default:
        color = "dark";
        disabled = true;
        action = "";
        break;
    }
    return {
      text: x.name,
      name: x.name,
      color,
      disabled,
      action,
    };
  });
  items.push({
    text: process.env.SHIELD_TEXT,
    name: process.env.SHIELD_NAME,
    color: has_shield ? "success" : "dark",
    disabled: false,
    action: `buyAction('${process.env.SHIELD_NAME}')`,
  });

  res.render("store", {
    user: req.session.user,
    items: items,
  });
});

router.post(
  "/buy",
  requireAuth,
  body("item").notEmpty().isString(),
  async (req, res) => {
    const data = validate(req, res);
    if (!data) {
      return;
    }

    const item = data.item;
    if (item === process.env.SHIELD_NAME) {
      // Activate shield!
      const result = await db.applyShield(req.session.user.id);
      if (result) {
        res.json({
          result: "success",
          redirect: "/",
        });
        return;
      }
      res.status(403).json({
        result: "failure",
        redirect: "/",
      });
      return;
    }
    const result = await db.buyItem(req.session.user.id, item);
    if (result) {
      res.json({
        result: "success",
        redirect: "/",
      });
      return;
    }
    res.status(403).json({
      result: "failure",
    });
  }
);

router.post(
  "/report",
  requireAuth,
  body("url").notEmpty().isString(),
  async (req, res) => {
    const data = validate(req, res);
    if (!data) {
      return;
    }
    if (req.session.user.username === process.env.ADMIN_USERNAME) {
      res.json({
        result: "failure"
      });
      return;
    }

    const url = data.url;
    const accountID = req.session.user.id;
    const result = await db.addReport(accountID, url);
    if (result) {
      res.json({
        result: "success",
        redirect: "/",
      });
      return;
    }
    res.status(403).json({
      result: "failure",
      redirect: "/",
    });
  }
);

module.exports = router;
