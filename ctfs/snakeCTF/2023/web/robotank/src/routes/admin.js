const express = require("express");
const router = express.Router();
const { body } = require("express-validator");

const db = require("../db");
const { requireAuth, requireAdmin } = require("../middlewares/auth");
const { validate } = require("../utils/validation");

router.use(requireAuth);
router.use(requireAdmin);

router.get("/", (req, res) => {
  db.fetchItemsAndOwners().then((items) => {
    res.render("admin", {
      items: items,
      user: req.session.user,
    });
  });
});

router.post("/", body("id").notEmpty(), (req, res) => {
  const data = validate(req, res);
  if (!data) {
    return;
  }

  action_id = parseInt(data.id);
  if (isNaN(action_id)) {
    res.json({
      result: "failure",
    });
    return;
  }
  db.resetItemOwner(action_id).then((success) => {
    if (success) {
      res.json({
        result: "success",
        redirect: "/admin",
      });
    } else {
      res.json({
        result: "failure",
        redirect: "/admin",
      });
    }
  });
});

module.exports = router;
