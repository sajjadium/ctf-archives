const express = require("express");
const cookieParser = require("cookie-parser");
const sessions = require('express-session');
const body_parser = require("body-parser");
const multer = require('multer')
const crypto = require("crypto")
const path = require("path");
const fs = require("fs");
const utils = require("./utils");

const app = express();

app.set('view engine', 'ejs');
app.set('views', './views');
app.disable('view cache');

app.use(sessions({
    secret: crypto.randomBytes(64).toString("hex"),
    cookie: { maxAge: 24 * 60 * 60 * 1000 },
    resave: false,
    saveUninitialized: true
}));
app.use('/static', express.static('static'))
app.use(body_parser.urlencoded({ extended: true }));
app.use(cookieParser());

const upload = multer();

app.get("/", (req, res) => {
    const article_paths = fs.readdirSync("articles");
    let articles = []
    for (const article_path of article_paths) {
        const contents = fs.readFileSync(path.join("articles", article_path)).toString().split("\n\n");
        articles.push({
            id: article_path,
            date: contents[0],
            title: contents[1],
            summary: contents[2],
            content: contents[3]
        });
    }
    res.render("index", {session: req.session, articles: articles});
})

app.get("/article", (req, res) => {
    const id = parseInt(req.query.id).toString();
    const article_path = path.join("articles", id);
    try {
        const contents = fs.readFileSync(article_path).toString().split("\n\n");
        const article = {
            id: article_path,
            date: contents[0],
            title: contents[1],
            summary: contents[2],
            content: contents[3]
        }
        res.render("article", { article: article, session: req.session, flag: process.env.FLAG });
    } catch {
        res.sendStatus(404);
    }
})

app.get("/login", (req, res) => {
    res.render("login", {session: req.session});
})

app.get("/register", (req, res) => {
    res.render("register", {session: req.session});
})

app.post("/register", (req, res) => {
    const username = req.body.username;
    const result = utils.register(username);
    if (result.success) res.download(result.data, username + ".key");
    else res.render("register", { error: result.data, session: req.session });
})

app.post("/login", upload.single('key'), (req, res) => {
    const username = req.body.username;
    const key = req.file;
    const result = utils.login(username, key.buffer);
    if (result.success) { 
        req.session.username = result.data.username;
        req.session.admin = result.data.admin;
        res.redirect("/");
    }
    else res.render("login", { error: result.data, session: req.session });
})

app.get("/logout", (req, res) => {
    req.session.destroy();
    res.redirect("/");
})

app.get("/edit", (req, res) => {
    if (!req.session.admin) return res.sendStatus(401);
    const id = parseInt(req.query.id).toString();
    const article_path = path.join("articles", id);
    try {
        const article = fs.readFileSync(article_path).toString();
        res.render("edit", { article: article, session: req.session, flag: process.env.FLAG });
    } catch {
        res.sendStatus(404);
    }
})

app.post("/edit", (req, res) => {
    if (!req.session.admin) return res.sendStatus(401);
    try {
        fs.writeFileSync(path.join("articles", req.query.id), req.body.article.replace(/\r/g, ""));
        res.redirect("/");
    } catch {
        res.sendStatus(404);
    }
})

app.listen(3000, () => {
    console.log("Server running on port 3000");
})