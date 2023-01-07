const express = require("express");
const crypto = require("crypto");
const axios = require("axios");
const { createClient } = require("redis");

const db = require("../src/db.js");
const mw = require("../src/middleware.js");

const router = express.Router();
const sha256 = (data) => crypto.createHash("sha256").update(data).digest("hex");

const REDIS_PASSWORD = process.env.REDIS_PASSWORD ? process.env.REDIS_PASSWORD: "redis_password"

const redisClient = createClient({
    url: `redis://:${REDIS_PASSWORD}@localhost:6379`,
})

redisClient.connect();

router.get("/post/:id", (req, res) => {
    let { id } = req.params;

    if (!id || typeof id !== "string") {
        return res.jsonp({
            success: false,
            error: "Missing id"
        });
    }

    if (!db.posts.has(id)) {
        return res.jsonp({
            success: false,
            error: "No post found with that id"
        });
    }

    let post = db.posts.get(id);
    return res.jsonp({
        success: true,
        name: post.name,
        body: post.body
    });
});

router.post("/login", [mw.csrfProtection, mw.requiresNoLogin], (req, res) => {
    let { user, pass } = req.body;

    if (!user || !pass) {
        return res.redirect("/login?msg=Missing user or pass");
    }

    if (typeof user !== "string" || typeof pass !== "string") {
        return res.redirect("/login?msg=Missing user or pass");
    }

    let dbUser = db.users.get(user);
    if (!dbUser || sha256(pass) !== dbUser.pass) {
        return res.redirect("/login?msg=Invalid user or pass");
    }

    req.session.user = user;
    res.redirect("/");
});

router.post("/register", [mw.csrfProtection, mw.requiresNoLogin], (req, res) => {
    let { user, pass } = req.body;

    if (!user || !pass) {
        return res.redirect("/register?msg=Missing user or pass");
    }

    if (typeof user !== "string" || typeof pass !== "string") {
        return res.redirect("/register?msg=Missing user or pass");
    }

    if (user.length < 5 || pass.length < 8) {
        return res.redirect("/register?msg=Please choose a more secure user/pass");
    }

    let dbUser = db.users.get(user);
    if (dbUser) {
        return res.redirect("/register?msg=A user already exists with that name");
    }

    db.users.set(user, {
        user,
        pass: sha256(pass),
        posts: [],
        todos: []
    });

    req.session.user = user;
    res.redirect("/");
});

router.post("/report", [mw.csrfProtection, mw.requiresLogin], async (req, res) => {
    let { url } = req.body;

    if (!url || typeof url !== "string") {
        return res.redirect("/report?msg=Missing URL");
    }

    if (!url.startsWith("http:") && !url.startsWith("https:")) {
        return res.redirect("/report?msg=Invalid URL");
    }

    if (req.session.lastSubmission && +new Date() - req.session.lastSubmission < 30000)  {
        return res.redirect("/report?msg=Please wait a bit before submitting a new URL");
    }

    if (process.env.RECAPTCHA_SITE_KEY && process.env.RECAPTCHA_SECRET_KEY) {
        let recaptcha = req.body["g-recaptcha-response"];

        if (!recaptcha || typeof recaptcha !== "string") {
            return res.redirect("/report?msg=Missing captcha");
        }

        try {
            let r = await axios({
                method: "POST",
                url: "https://www.google.com/recaptcha/api/siteverify",
                params: {
                    secret: process.env.RECAPTCHA_SECRET_KEY,
                    response: recaptcha
                }
            });
            if (!r.data || !r.data.success) {
                return res.redirect("/report?msg=Invalid captcha");
            }
        }
        catch(err) {
            return res.redirect("/report?msg=Failed to validate captcha");
        }
    }

    req.session.lastSubmission = +new Date();
    redisClient.lPush('submissions', [url]);
    res.redirect("/report?msg=URL submitted successfully");
});

router.get("/logout", [mw.csrfProtection, mw.requiresLogin], (req, res) => {
    req.session.destroy();
    res.redirect("/");
});

// Don't allow admin to make new posts / todos
router.use((req, res, next) => {
    if (req.user.user === "admin")  {
        return res.redirect("/?msg=Nice try");
    }
    next();
});

router.post("/create/post", [mw.csrfProtection, mw.requiresLogin], (req, res) => {
    let { name, body } = req.body;

    if (!name || !body) {
        return res.redirect("/?msg=Missing name or body");
    }

    if (typeof name !== "string" || typeof body !== "string") {
        return res.redirect("/?msg=Missing name or body");
    }

    let id = crypto.randomUUID();
    db.posts.set(id, {
        name, body
    });
    req.user.posts.push(id);

    res.redirect("/post/?id=" + id);
});

router.post("/create/todo", [mw.csrfProtection, mw.requiresLogin], (req, res) => {
    let { text } = req.body;

    if (!text) {
        return res.redirect("/?msg=Missing text");
    }

    if (typeof text !== "string") {
        return res.redirect("/?msg=Missing text");
    }

    let isURL = false;
    try {
        new URL(text); // errors if not valid URL
        isURL = !text.toLowerCase().trim().startsWith("javascript:"); // no
    } catch {}

    req.user.todos.push({
        text, isURL
    });

    res.redirect("/");
});

module.exports = router;
