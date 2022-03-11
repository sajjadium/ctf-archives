const express = require("express");
const jwt = require("jwt-simple");
const crypto = require("crypto");

const app = express();

// Alex only likes Chrome. All FireFox users should get out of here!

const PORT = process.env.PORT || 8080;

const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 4096 });
const pub = publicKey.export({ type: "pkcs1", format: "pem" });
const priv = privateKey.export({ type: "pkcs1", format: "pem" });

const bot = require("./bot.js");

app.set("view engine", "hbs");

app.use(express.static("public"));
app.use(express.urlencoded({ extended: false }));
app.use(require("cookie-parser")());

app.use((req, res, next) => {
    if(!req.cookies.auth) {
        let username = crypto.randomBytes(8).toString("hex");
        let cookie = jwt.encode({ username }, priv, "RS256");
        req.cookies.auth = cookie;
        res.cookie("auth", cookie);
    }

    try {
        let auth = jwt.decode(req.cookies.auth, pub);
        res.locals.username = auth.username;
    }
    catch(err) {
        res.clearCookie("auth");
        return res.redirect("/?message=Invalid token");
    }

    let nonce = crypto.randomBytes(16).toString("hex");
    res.setHeader("Content-Security-Policy", `
        default-src 'self';
        img-src 'self' data:;
        style-src 'nonce-${nonce}';
        font-src https://fonts.googleapis.com/ https://fonts.gstatic.com/;
        object-src 'none';
        base-uri 'none';
        script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/;
    `.trim().replace(/\s+/g, " "));
    res.locals.nonce = nonce;
    next();
});

const isUser = (user) => (req, res, next) => res.locals.username === user ? next() : res.redirect("/");

app.get("/home", isUser("Alex"), (req, res) => {
    res.render("home");
});

app.post("/home", isUser("Alex"), (req, res) => {
    let { message } = req.body;
    if(!message || typeof message !== "string") {
        return res.redirect("/home?message=Missing message");
    }

    // no XSS
    message = message.replace(/"/g, "&quot;");
    message = message.replace(/</g, "&lt;");
    message = message.replace(/>/g, "&gt;");

    // convert images and links
    message = message.replace(/(https?:\/\/[^\s]*\.(png|jpg|gif)[^\s]*)/g, `<iframe src="$1"></iframe>`);
    message = message.replace(/(https?:\/\/(?![^\s]*(?:jpg|png|gif))[^\s]+)/g, `<a href="$1">$1</a>`);

    return res.render("home", { message });
});

app.post("/report", isUser("Alex"), (req, res) => {
    let { message } = req.body;
    if(!message || typeof message !== "string") {
        return res.redirect("/home?message=Missing message");
    }

    bot.visit(message, jwt.encode({ username: "Alex" }, priv, "RS256"));
    return res.redirect("/home?message=The admin will look at your message now");
});

app.get("/", (req, res) => {
    if(res.locals.username === "Alex") {
        return res.redirect("/home");
    }
    res.render("login");
});

app.listen(PORT, () => console.log(`listening on port ${PORT}`));