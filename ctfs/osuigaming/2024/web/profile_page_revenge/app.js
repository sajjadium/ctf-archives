import express from "express";
import expressSession from "express-session";
import cookieParser from "cookie-parser";
import crypto from "crypto";
import { JSDOM } from "jsdom";
import DOMPurify from "dompurify";

const app = express();
const PORT = process.env.PORT || 3727;

app.use(express.urlencoded({ extended: false }));
app.use(expressSession({
    secret: crypto.randomBytes(32).toString("hex"),
    resave: false,
    saveUninitialized: false
}));
app.use(express.static("public"));
app.use(cookieParser());
app.set("view engine", "hbs");

app.use((req, res, next) => {
    res.locals.nonce = crypto.randomBytes(32).toString("hex");
    res.setHeader("Content-Security-Policy", `
        default-src https://osugaming.lol 'self';
        style-src https://osugaming.lol 'nonce-${res.locals.nonce}';
        script-src 'self' 'nonce-${res.locals.nonce}';
        object-src 'none';
        frame-src 'self' https://www.youtube.com;
        form-action 'self';
        frame-ancestors 'none';
        base-uri 'self';
    `.trim().replace(/\s+/g, " "));
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    res.setHeader("X-Frame-Options", "DENY");
    if (req.session.user && users.has(req.session.user)) {
        req.user = users.get(req.session.user);
        res.locals.user = req.user;
    }
    next();
});

const window = new JSDOM('').window;
const purify = DOMPurify(window);
const renderBBCode = (data) => {
    data = data.replaceAll(/\[b\](.+?)\[\/b\]/g, '<strong>$1</strong>');
    data = data.replaceAll(/\[i\](.+?)\[\/i\]/g, '<i>$1</i>');
    data = data.replaceAll(/\[u\](.+?)\[\/u\]/g, '<u>$1</u>');
    data = data.replaceAll(/\[strike\](.+?)\[\/strike\]/g, '<strike>$1</strike>');
    data = data.replaceAll(/\[color=#([0-9a-f]{6})\](.+?)\[\/color\]/g, '<span style="color: #$1">$2</span>');
    data = data.replaceAll(/\[size=(\d+)\](.+?)\[\/size\]/g, '<span style="font-size: $1px">$2</span>');
    data = data.replaceAll(/\[url=(.+?)\](.+?)\[\/url\]/g, '<a href="$1">$2</a>');
    data = data.replaceAll(/\[img\](.+?)\[\/img\]/g, '<img src="$1" />');
    return data;
};
const renderBio = (data) => {
    data = data.replaceAll(/</g, "&lt;").replaceAll(/>/g, "&gt;");
    const html = renderBBCode(data);
    const sanitized = purify.sanitize(html);
    // do this after sanitization because otherwise iframe will be removed
    return sanitized.replaceAll(
        /\[youtube\](.+?)\[\/youtube\]/g,
        '<iframe sandbox="allow-scripts" width="640px" height="480px" src="https://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>'
    );
};

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const users = new Map();

const requiresLogin = (req, res, next) => req.user ? next() : res.redirect("/login");

app.post("/api/register", (req, res) => {
    const { username, password } = req.body;

    if (!username || typeof username !== "string" || !password || typeof password !== "string") {
        return res.end("missing username or password");
    }
    
    if (username.length < 5 || password.length < 8) {
        return res.end("username or password too short");
    }

    if (username.length > 30 || /[^A-Za-z0-9 ]/.test(username)) {
        return res.end("invalid username format");
    }

    if (users.has(username)) {
        return res.end("a user already exists with that username");
    }

    users.set(username, {
        username,
        password: sha256(password),
        bio: renderBio(`Welcome to ${username}'s page!`)
    });

    req.session.user = username;
    res.cookie("csrf", crypto.randomBytes(32).toString("hex"));
    res.redirect("/profile");
});

app.post("/api/login", (req, res) => {
    const { username, password } = req.body;

    if (!username || typeof username !== "string" || !password || typeof password !== "string") {
        return res.end("missing username or password");
    }

    if (!users.has(username)) {
        return res.end("no user exists with that username");
    }

    if (users.get(username).password !== sha256(password)) {
        return res.end("invalid password");
    }

    req.session.user = username;
    res.cookie("csrf", crypto.randomBytes(32).toString("hex"));
    res.redirect("/profile");
});

// TODO: update bio from UI
app.post("/api/update", requiresLogin, (req, res) => {
    const { bio } = req.body;

    if (!bio || typeof bio !== "string") {
        return res.end("missing bio");
    }

    if (!req.headers.csrf) {
        return res.end("missing csrf token");
    }

    if (req.headers.csrf !== req.cookies.csrf) {
        return res.end("invalid csrf token");
    }

    if (bio.length > 2048) {
        return res.end("bio too long");
    }

    req.user.bio = renderBio(bio);
    res.send(`Bio updated!`);
});

app.get("/login", (req, res) => res.render("login"));
app.get("/register", (req, res) => res.render("register"));
app.get("/profile", requiresLogin, (req, res) => res.render("profile"));
app.get("/", (req, res) => res.redirect("/profile"));

app.get('*', (req, res) => {
    res.set("Content-Type", "text/plain");
    res.status = 404;
    res.send(`Error: ${req.originalUrl} was not found`);
});

app.listen(PORT, () => console.log(`web/profile-page-revenge listening at http://localhost:${PORT}`));