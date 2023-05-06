const express = require("express");
const crypto = require("crypto");

const app = express();

const PORT = process.env.PORT || 1234;

const users = new Map();

const session = require("express-session");
const MemoryStore = require("memorystore")(session);
app.use(
    session({
        cookie: { maxAge: 900000 },
        store: new MemoryStore({
            checkPeriod: 900000, // clear every 15 minutes
        }),
        resave: true,
        saveUninitialized: true,
        secret: crypto.randomBytes(32).toString("hex"),
        dispose: (key, value) => {
            users.delete(key);
        }
    })
);

app.use(express.urlencoded({ extended: false }));
app.set('view engine', 'hbs');

app.use((req, res, next) => {
    res.locals.nonce = crypto.randomBytes(32).toString("hex");

    // Surely this will be enough to protect my website
    // Clueless
    res.setHeader("Content-Security-Policy", `
        default-src 'self';
        script-src 'nonce-${res.locals.nonce}' 'unsafe-inline';
        object-src 'none';
        base-uri 'none';
        frame-ancestors 'none';
    `.trim().replace(/\s+/g, " "));
    res.setHeader("Cache-Control", "no-store");
    res.setHeader("X-Frame-Options", "DENY");
    res.setHeader("X-Content-Type-Options", "nosniff");
    res.setHeader("Referrer-Policy", "no-referrer");
    res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    res.setHeader("Cross-Origin-Resource-Policy", "same-origin");
    res.setHeader("Document-Policy", "force-load-at-top");

    if (!req.session.id) {
        req.session.id = crypto.randomUUID();
    }
    if (!users.has(req.session.id)) {
        users.set(req.session.id, {
            list: []
        });
    }

    req.user = users.get(req.session.id);
    next();
});

app.use(express.static("public"));

app.post("/create", (req, res) => {
    let { text } = req.body;

    if (!text || typeof text !== "string") {
        return res.end("Missing 'text' variable")
    }

    req.user.list.push(text.slice(0, 2048));
    req.user.list.sort();

    res.redirect("/");
});

app.post("/remove", (req, res) => {
    let { index } = req.body;

    if (!index || typeof index !== "string") {
        return res.end("Missing 'index' variable");
    }
    
    index = parseInt(index);
    if (isNaN(index)) {
        return res.end("Missing 'index' variable");
    }

    req.user.list.splice(index, 1);
    res.redirect("/");
});

app.get("/", (req, res) => {
    res.render("home", { list: encodeURIComponent(JSON.stringify(req.user.list)) });
});

app.listen(PORT, () => console.log(`web/safelist listening on port ${PORT}`));