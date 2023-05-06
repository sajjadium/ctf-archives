const express = require('express');
const crypto = require('crypto');

const app = express();

require("dotenv").config();

const PORT = process.env.PORT ?? 80;

const session = require('express-session')
const MemoryStore = require('memorystore')(session);
const store = new MemoryStore({
    checkPeriod: 3600000
});

const expressWs = require('express-ws')(app);
const ws = require("./src/ws.js");
ws.init(expressWs.getWss());

app.use(session({
    cookie: { 
        maxAge: 86400000,
        path: '/chat',
        httpOnly: true
    },
    store,
    resave: false,
    saveUninitialized: false,
    secret: process.env.SESSION_SECRET ?? crypto.randomBytes(16).toString("hex")
}));

app.use((req, res, next) => {
    res.locals.nonce = crypto.randomBytes(16).toString("hex");
    res.locals.site = process.env.SITE;
    if(req.session && req.session.user) {
        res.locals.user = req.session.user;
    }

    res.setHeader("Content-Security-Policy", `
        default-src 'none';
        base-uri 'none';
        connect-src 'self';
        frame-src 'self';
        script-src
            'nonce-${res.locals.nonce}'
            'unsafe-inline';
        style-src
            'nonce-${res.locals.nonce}'
            'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='
            'sha256-5uZsN51mZNPiwsxlFtZveRchbCHcHkPoIjG7N2Y4rIU=';
        frame-ancestors 'none';
    `.trim().replace(/(\n\s+|\n|\s+)/g, " "));

    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');

    next();
});
app.set("view engine", "hbs");
app.use(express.urlencoded({ extended: false }));
app.use(express.static('public'));

app.use("/chat", require("./routes/chat.js"));
app.get("/sandbox", (req, res) => {
     res.setHeader("Content-Security-Policy", `
        default-src 'none';
        base-uri 'none';
        script-src
            'nonce-${res.locals.nonce}'
            'unsafe-inline';
        frame-ancestors 'self';
    `.trim().replace(/(\n\s+|\n|\s+)/g, " "));
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.render("sandbox");
});
app.get("/", (req, res) => res.redirect("/chat/"));

app.listen(PORT, () => {
    console.log(`chall listening on ${PORT}`);
});