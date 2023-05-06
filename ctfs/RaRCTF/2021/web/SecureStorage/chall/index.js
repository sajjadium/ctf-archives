const express = require("express");
require("dotenv").config();

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3999;
const SECURE_PORT = process.env.SECURE_PORT ? parseInt(process.env.SECURE_PORT) : 4000;

const app = express(); // public server to send messages to secure backend
const secure_app = express(); // sandboxed secure app

const session = require('express-session');
const MemoryStore = require('memorystore')(session);
app.use(express.urlencoded({ extended: false }));
app.use(session({
    cookie: { maxAge: 86400000 },
    store: new MemoryStore({
      checkPeriod: 86400000 
    }),
    resave: false,
    saveUninitialized: false,
    secret: require("crypto").randomBytes(32).toString("hex")
}));
app.use(express.static('public'));
app.set('trust proxy', true);

app.set('view engine', 'hbs');
secure_app.set('view engine', 'hbs');

app.use(express.static("./public/"));
secure_app.use(express.static("./secure_safe/"));

app.use(async (req, res, next) => {
    /* flash stuff */
    res.locals.info = req.session.info;
    res.locals.error = req.session.error;
    req.session.info = null;
    req.session.error = null;

    res.locals.user = req.session.user;

    res.locals.SANDBOX_SITE = process.env.SANDBOX_SITE;

    next();
});

const requiresLogin = (req, res, next) => {
    if(!req.session.user) {
        req.session.error = "Login required to access this page";
        return res.redirect("/");
    }
    next();
};

secure_app.get("/", (req, res) => res.render("secure", { DEFAULT_SITE: process.env.DEFAULT_SITE, layout: null }));

app.use("/api", require("./routes/api.js"));

app.get("/login", (req, res) => res.render("login"));
app.get("/register", (req, res) => res.render("register"));
app.get("/home", requiresLogin, (req, res) => res.render("home"));
app.get("/submit", requiresLogin, (req, res) => res.render("submit"));
app.get("/", (req, res) => res.render("index"));

app.listen(PORT, () => {
    console.log(`safestorage chall listening on port ${PORT}`);
});

secure_app.listen(SECURE_PORT, () => {
    console.log(`secure app listening on port ${SECURE_PORT}`);
});