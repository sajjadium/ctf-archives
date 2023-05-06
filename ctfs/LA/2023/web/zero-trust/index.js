const express = require("express");
const path = require("path");
const fs = require("fs");
const cookieParser = require("cookie-parser");
const crypto = require("crypto");

const port = parseInt(process.env.PORT) || 8080;

const key = crypto.randomBytes(32);

const app = express();

const lists = new Map();

setInterval(function () {
    for (const file of fs.readdirSync("/tmp/pastestore")) {
        if (Date.now() - fs.statSync("/tmp/pastestore/" + file).mtimeMs > 1000 * 60 * 60) {
            fs.rmSync("/tmp/pastestore/" + file);
        }
    }
}, 60000);

function makeAuth(req, res, next) {
    const iv = crypto.randomBytes(16);
    const tmpfile = "/tmp/pastestore/" + crypto.randomBytes(16).toString("hex");
    fs.writeFileSync(tmpfile, "there's no paste data yet!", "utf8");
    const user = { tmpfile };
    const data = JSON.stringify(user);
    const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
    const ct = Buffer.concat([cipher.update(data), cipher.final()]);
    const authTag = cipher.getAuthTag();
    res.cookie("auth", [iv, authTag, ct].map((x) => x.toString("base64")).join("."));
    res.locals.user = user;
    next();
}

function needsAuth(req, res, next) {
    const auth = req.cookies.auth;
    if (typeof auth !== "string") {
        makeAuth(req, res, next);
        return;
    }
    try {
        const [iv, authTag, ct] = auth.split(".").map((x) => Buffer.from(x, "base64"));
        const cipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
        cipher.setAuthTag(authTag);
        res.locals.user = JSON.parse(cipher.update(ct).toString("utf8"));
        if (!fs.existsSync(res.locals.user.tmpfile)) {
            makeAuth(req, res, next);
            return;
        }
    } catch (err) {
        makeAuth(req, res, next);
        return;
    }
    next();
}

app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "static")));

const template = fs.readFileSync("index.html", "utf8");

app.get("/", needsAuth, (req, res) => {
    res.type("text/html").send(template.replace("$CONTENT", () => fs.readFileSync(res.locals.user.tmpfile, "utf8")));
});

app.post("/update", needsAuth, (req, res) => {
    if (typeof req.body.content === "string") {
        try {
            fs.writeFileSync(res.locals.user.tmpfile, req.body.content.slice(0, 2048), "utf8");
        } catch (err) {}
    }
    res.redirect("/");
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
