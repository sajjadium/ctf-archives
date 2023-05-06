const express = require("express");
const bcrypt = require("bcrypt");
const fetch = require('node-fetch');

const router = express.Router();

const { User, Style, requiresLogin } = require("../src/db.js");

router.post("/register", async (req, res) => {
    let { user, pass } = req.body;

    if(!user || !pass) {
        req.session.error = "Missing username or password.";
        return res.redirect("/register");
    }

    if(await User.findByPk(user)) {
        req.session.error = "A user already exists with that name.";
        return res.redirect("/register");
    }

    let hash = await bcrypt.hash(pass, 12);
    try {
        await User.create({ user, pass: hash });
        req.session.info = `Registered as ${user} successfully.`;
        req.session.user = user;
        res.redirect("/");
    }
    catch(err) {
        req.session.error = err.message;
        res.redirect("/register");
    }
});

router.post("/login", async (req, res) => {
    let { user, pass } = req.body;

    if(!user || !pass) {
        req.session.error = "Missing username or password.";
        return res.redirect("/login");
    }

    let entry = await User.findByPk(user);
    if(!entry) {
        req.session.error = "No user with the given username exists.";
        return res.redirect("/login");
    }

    if(!await bcrypt.compare(pass, entry.pass)) {
        req.session.error = "Incorrect password.";
        return res.redirect("/login");
    }

    req.session.info = `Logged in as ${user} successfully.`;
    req.session.user = user;
    res.redirect("/");
});

router.post("/create", requiresLogin, async (req, res) => {
    let { title, css, url, hidden } = req.body;

    if(!title || !css || !url) {
        req.session.error = "Missing details to create a new style.";
        return res.redirect("/create");
    }

    try {
        new URL(url);
    }
    catch(e) {
        req.session.error = "Invalid URL.";
        return res.redirect("/create");
    }

    if(!/^[a-zA-Z0-9 ]*$/.test(title)) {
        req.session.error = "Invalid title.";
        return res.redirect("/create");
    }

    /* stylescript validation */
    let blacklist = ["--styleme stylescript v1.0--", "---------------", "global"];
    if(blacklist.some(b => title.includes(b) || url.toLowerCase().includes(b) || css.includes(b))) {
        req.session.error = "Stylescript contains some invalid characters.";
        return res.redirect("/create");
    }   

    hidden = Boolean(hidden);
    try {
        let style = await Style.create({ title, url, css, hidden });
        await style.setUser(req.user);
        await req.user.addStyle(style);
        req.session.info = "New style created successfully!";
        res.redirect("/");
    }
    catch(err) {
        req.session.error = err.message;
        res.redirect("/create");
    }
});

router.post("/delete", requiresLogin, async (req, res) => {
    if(req.user.user === "admin") {
        return res.redirect("/");
    }

    let { id } = req.body;

    let style = (await req.user.getStyles()).find(s => s.id === id);
    if(!style) {
        req.session.error = "No style was found.";
        return res.redirect("/");
    }

    await style.destroy();
    req.session.info = "Style deleted successfully.";
    res.redirect("/");
});

router.post("/submit", requiresLogin, async (req, res) => {
    let { url } = req.body;

    if(req.session.lastSubmit && new Date() - new Date(req.session.lastSubmit) <= 15*1000) {
        req.session.error = `You must wait 15 seconds between submissions.`;
        return res.redirect("/submit");
    }

    if(!url) {
        req.session.error = "Missing url.";
        return res.redirect("/submit");
    }

    if(!url.startsWith(`${process.env.SITE}/styles/i/`)) {
        req.session.error = `URL must start with ${process.env.SITE}/styles/i/`;
        return res.redirect("/submit");
    }

    let urlObj;
    try {
        urlObj = new URL(url);
    }
    catch(err) {
        req.session.error = `Invalid URL`;
        return res.redirect("/submit");
    }

    if(urlObj.origin !== process.env.SITE || !urlObj.pathname.startsWith("/styles/i/")) {
        req.session.error = `URL must start with ${process.env.SITE}/styles/i/`;
        return res.redirect("/submit");
    }

    req.session.lastSubmit = new Date();
    
    // uhhh
    // do something here to look at your URL with the extension installed
    // the admin bot only installs stuff from https://styleme.be.ax
    // and also skips all the confirmation dialogs :>

    req.session.info = "An admin will look at your style soon.";
    return res.redirect("/submit");
});

router.get("/logout", async (req, res) => {
    req.session.destroy();
    res.redirect("/");
});

module.exports = router;