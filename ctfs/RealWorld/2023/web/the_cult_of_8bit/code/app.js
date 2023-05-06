const express = require("express");
const crypto = require("crypto");

const db = require("./src/db.js");
const mw = require("./src/middleware.js");

const app = express();

const PORT = process.env.PORT || 12345;

app.set("view engine", "ejs");
app.set("etag", false);
app.use(require("express-session")({
    secret: crypto.randomBytes(64).toString("hex"),
    resave: false,
    saveUninitialized: false
}));
app.use(require('cookie-parser')());
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
    res.setHeader("Cache-Control", "no-store");
    res.setHeader("X-Content-Type-Options", "nosniff");
    res.setHeader("Referrer-Policy", "no-referrer");
    next();
});

app.use(express.static("static"));

app.use((req, res, next) => {
    req.csrfToken = req.cookies._csrf;

    res.locals.user = null;
    if (req.session.user && db.users.has(req.session.user)) {
        req.user = db.users.get(req.session.user);
        res.locals.user = req.user;
    }

    res.locals.RECAPTCHA_SITE_KEY = null;
    if (process.env.RECAPTCHA_SITE_KEY && process.env.RECAPTCHA_SECRET_KEY) {
        res.locals.RECAPTCHA_SITE_KEY = process.env.RECAPTCHA_SITE_KEY;
    }

    next();
});

app.use("/api/", require("./routes/api.js"));

app.use((req, res, next) => {
    const csrf = crypto.randomBytes(16).toString("hex");
    res.locals._csrf = csrf;
    req.session.hasCSRF = true;
    res.cookie("_csrf", csrf);
    next();
})

app.get("/login/", mw.requiresNoLogin, (req, res) => res.render("login"));
app.get("/register/", mw.requiresNoLogin, (req, res) => res.render("register"));

app.get("/report/", mw.requiresLogin, (req, res) => res.render("report"));
app.get("/post/", (req, res) => res.render("post"));
app.get("/", (req, res) => res.render("home"));

app.listen(PORT, () => console.log(`web/8bitcult listening on port ${PORT}`));
