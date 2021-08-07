const express = require("express");
const bcrypt = require("bcrypt");
const fetch = require("node-fetch");

const router = express.Router();

let users = [];

router.post("/register", async (req, res) => {
    let { user, pass } = req.body;

    if(!user || !pass) {
        req.session.error = "Missing username or password";
        return res.redirect("/register");
    }

    if(users.find(u => u.user === user)) {
        req.session.error = "A user already exists with that username";
        return res.redirect("/register");
    }

    pass = await bcrypt.hash(pass, 12);
    users.push({user, pass});

    req.session.user = user;
    req.session.info = `Logged in as ${user} successfully`;
    return res.redirect("/home");
});

router.post("/login", async (req, res) => {
    let { user, pass } = req.body;

    if(!user || !pass) {
        req.session.error = "Missing username or password";
        return res.redirect("/login");
    }

    if(!users.find(u => u.user === user)) {
        req.session.error = "No user exists with that username";
        return res.redirect("/login");
    }

    let entry = users.find(u => u.user === user);
    if(!await bcrypt.compare(pass, entry.pass)) {
        req.session.error = "Incorrect password";
        return res.redirect("/login");
    }

    req.session.user = user;
    req.session.info = `Logged in as ${user} successfully`;
    return res.redirect("/home");
});

router.post("/submit", (req, res) => {
    let { url } = req.body;
    if(req.session.lastSubmit && new Date() - new Date(req.session.lastSubmit) <= 30*1000) {
        req.session.error = `You must wait 30 seconds between submissions`;
        return res.redirect("/submit");
    }

    if(!url) {
        req.session.error = "Missing URL";
        return res.redirect("/submit");
    }

    try {
        let check = new URL(url);
        if(check.protocol !== "http:" && check.protocol !== "https:")
            throw new Error("nope");
    }
    catch(err) {
        req.session.error = `Invalid URL`;
        return res.redirect("/submit");
    }

    fetch(`http://admin/xss/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": process.env.XSSBOT_SECRET
        },
        body: JSON.stringify({
            url
        })
    });
    req.session.lastSubmit = new Date();

    req.session.info = "URL submitted to the admin succesfully";
    return res.redirect("/submit");
});

router.get("/logout", (req, res) => {
    req.session.destroy();
    res.redirect("/");
});

module.exports = router;