const express = require("express");
const router = express.Router();
const { requireAuth } = require("../../middlewares/auth");
const db = require("../../db");
const { doFetch } = require("../../utils/backend");

const robotank_actions = ["forward", "backward", "left", "right", "stop"];

router.use(requireAuth);

const handleRobotankAction = async (action, req, res, next) => {
   // This function is not part of the challenge
  const path = `${action}?restricted=true`;
  const result = await doFetch({ path });
  res.json({ result: "success" });
};

const handleCameraAction = async (req, res, next) => {
  // This function is not part of the challenge
  const result = await doFetch({ path: "photo" });
  const blob = await result.blob();
  const img = Buffer.from(await blob.arrayBuffer());
  res.set("Content-Type", "image/jpeg");
  res.send(img);
};

router.get("/:action", async (req, res, next) => {
  const action = req.params.action;

  try {
    const db_action = await db.fetchItemAndOwner(action);
    // confirm that the user owns this action and is not the admin
    if (
      db_action.username !== req.session.user.username ||
      req.session.user.username === process.env.ADMIN_USERNAME
    ) {
      res.status(401).json({
        result: "failure",
        message: "Forbidden",
      });
      return;
    }
    // Handle the action
    if (robotank_actions.includes(action)) {
      handleRobotankAction(action, req, res, next);
      return;
    }
    if (action === "camera") {
      handleCameraAction(req, res, next);
      return;
    }
    throw "Not implemented";
  } catch (err) {
    res.status(500).json({
      result: "failure",
      message: "Robotank is dead D:",
    });
  }
});

module.exports = router;
