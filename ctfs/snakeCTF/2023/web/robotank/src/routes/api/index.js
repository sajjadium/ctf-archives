const express = require("express");
const router = express.Router();

const actionsrouter = require("./actions");

router.use("/actions", actionsrouter);

module.exports = router;
