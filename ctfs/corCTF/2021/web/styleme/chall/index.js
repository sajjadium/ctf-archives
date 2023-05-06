const express = require("express");
const app = express();

const crypto = require("crypto");

require("dotenv").config();

const session = require('express-session');
const MemoryStore = require('memorystore')(session);

const PORT = process.env.PORT || 80;

app.use(express.urlencoded({ extended: false }));
app.use(session({
    cookie: { maxAge: 86400000 },
    store: new MemoryStore({
      checkPeriod: 86400000 
    }),
    resave: false,
    saveUninitialized: false,
    secret: process.env.SESSION_SECRET || "keyboard cat"
}));
app.use(express.static('public'));
app.set('view engine', 'hbs');
app.set('trust proxy', true);

const { User, requiresLogin } = require("./src/db.js");

app.use(async (req, res, next) => {
    /* flash stuff */
    res.locals.info = req.session.info;
    res.locals.error = req.session.error;
    req.session.info = null;
    req.session.error = null;

    if(req.session.user) {
        res.locals.user = req.session.user;
        req.user = await User.findByPk(req.session.user);
    }

    // nginx sets this
    // checks whether request is coming from localhost :>
    req.isAdmin = !Boolean(req.headers['x-forwarded-for']);

    res.locals.nonce = crypto.randomBytes(16).toString("hex");
    res.setHeader("Content-Security-Policy", `default-src 'none'; style-src 'self'; font-src 'self'; base-uri 'self'; script-src 'nonce-${res.locals.nonce}' 'unsafe-inline';`);
    next();
});

app.use((err, req, res, next) => {
    res.status(500).send('Something broke!');
});

app.use("/api", require("./routes/api.js"));
app.use("/styles", require("./routes/styles.js"));

app.get("/create", requiresLogin, (req, res) => res.render('create'));
app.get("/submit", requiresLogin, (req, res) => res.render('submit'));

app.get('/register', (req, res) => res.render('register'));
app.get('/login', (req, res) => res.render('login'));
app.get('/', (req, res) => res.render('index'));

app.listen(PORT, () => {
    console.log(`styleme listening on port ${PORT}`);
});