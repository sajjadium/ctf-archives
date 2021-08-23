const express = require("express");
const bcrypt = require("bcrypt");

const router = express.Router();

const db = require("../db.js");

const requiresLogin = (req, res, next) => {
    if(!req.user) {
        return res.redirect("/?error=" + encodeURIComponent("You must be logged in"));
    }
    next();
};

router.post("/register", async (req, res) => {
    let { user, pass } = req.body;
    if(!user || !pass) {
        return res.redirect("/?error=" + encodeURIComponent("Missing username or password"));
    }
    if(db.users.has(user)) {
        return res.redirect("/?error=" + encodeURIComponent("A user already exists with that username"));
    }
    db.users.set(user, {
        user,
        flags: [],
        money: 100,
        pass: await bcrypt.hash(pass, 12)
    });
    res.cookie('user', user, { signed: true, maxAge: 1000*60*60*24 });
    res.redirect("/");
});

router.post("/login", async (req, res) => {
    let { user, pass } = req.body;
    if(!user || !pass) {
        return res.redirect("/?error=" + encodeURIComponent("Missing username or password"));
    }
    if(!db.users.has(user)) {
        return res.redirect("/?error=" + encodeURIComponent("No user exists with that username"));
    }
    if(!await bcrypt.compare(pass, db.users.get(user).pass)) {
        return res.redirect("/?error=" + encodeURIComponent("Incorrect password"));
    }

    res.cookie('user', user, { signed: true, maxAge: 1000*60*60*24 });
    res.redirect("/");
});

router.post("/buy", requiresLogin, async (req, res) => {
    if(!req.body.flag) {
        return res.redirect("/flags?error=" + encodeURIComponent("Missing flag to buy"));
    }

    try {
        db.buyFlag({ user: req.user, ...req.body });
    }
    catch(err) {
        return res.redirect("/flags?error=" + encodeURIComponent(err.message));
    }

    res.redirect("/?message=" + encodeURIComponent("Flag bought successfully"));
});

module.exports = router;