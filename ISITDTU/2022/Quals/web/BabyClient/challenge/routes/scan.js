const express = require("express");
const router = express.Router();

const util = require("../src/util.js");
const bot = require("../src/bot.js");

let scanning = false;

router.get("/", (req, res) => res.render("scan"));
router.post("/", async (req, res) => {
    let { link } = req.body;

    if(scanning) {
        return util.flash(req, res, "error", "Please wait for the automated scanner to finish its current submission.");
    }

    if(!link) {
        return util.flash(req, res, "error", "Missing link to scan.");
    }

    let url;
    try {
        url = new URL(link);
    }
    catch (err) {
        return util.flash(req, res, "error", "Invalid link");
    }

    if(!['http:', 'https:'].includes(url.protocol)) {
        return util.flash(req, res, "error", "Link must be of protocol <b>http:</b> or <b>https:</b>");
    }

    scanning = true;

    util.flash(req, res, "info", "The automated scanner is now going over your submission.");
    await bot.visitPage(link);

    scanning = false;
});

module.exports = router;