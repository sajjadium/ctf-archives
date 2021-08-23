const express = require("express");
const crypto = require("crypto");
const csurf = require("csurf");

const app = express();

require("dotenv").config();
const PORT = process.env.PORT || 80;

const session = require('express-session');
const SessionStore = require('express-session-sequelize')(session.Store);

const db = require("./src/db.js");

app.use(session({
    secret: process.env.SESSION_SECRET || crypto.randomBytes(16).toString("hex"),
    store: new SessionStore({
        db: db.sequelize,
    }),
    resave: false,
    saveUninitialized: false,
}));
app.use(express.static("public"));
app.use(express.urlencoded({ extended: false }));
app.use(csurf());
app.set('view engine', 'ejs');

app.use(async (req, res, next) => {
    res.setHeader("Content-Security-Policy", `
        object-src 'none';
        script-src 'self' 'unsafe-eval';
    `.replace(/\n/g, "").trim());
    if(req.query.error)
        res.locals.error = req.query.error;
    if(req.query.message)
        res.locals.message = req.query.message;

    if(req.session.user) {
        try {
            req.user = await db.User.findByPk(req.session.user);
            res.locals.user = req.user.user;
        }
        catch(err) {
            req.session.user = null;
        }
    }

    res.locals.csrfToken = req.csrfToken();

    console.log(req.originalUrl, req.body, req.session);
    next();
});

app.use("/api", require("./routes/api.js"));
app.use("/", require("./routes/index.js"));

app.use((err, req, res, next) => {
    return res.redirect("/?error=" + encodeURIComponent(err.message));
});

app.listen(PORT, () => {
    console.log(`listening on port ${PORT}`);
});
