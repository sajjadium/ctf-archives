const express = require("express");
const path = require("path");
const fs = require("fs");
const cookieParser = require("cookie-parser");
const { v4: uuid } = require("uuid");

const flag = process.env.FLAG;
const port = parseInt(process.env.PORT) || 8080;
const adminpw = process.env.ADMINPW || "placeholder";

const accounts = new Map();
accounts.set("admin", {
    password: adminpw,
    displayName: flag,
    posts: [],
    friends: [],
});
const posts = new Map();

const app = express();

let cleanup = [];

setInterval(() => {
    const now = Date.now();
    let i = cleanup.findIndex((x) => now < x[1]);
    if (i === -1) {
        i = cleanup.length;
    }
    for (let j = 0; j < i; j++) {
        const account = accounts.get(cleanup[i][0]);
        for (const post of account.posts) {
            posts.delete(post);
        }
        accounts.delete(cleanup[i][0]);
    }
    cleanup = cleanup.slice(i);
}, 1000 * 60);

function needsAuth(req, res, next) {
    if (!res.locals.user) {
        res.redirect("/login");
    } else {
        next();
    }
}

app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use((req, res, next) => {
    res.locals.user = null;
    if (req.cookies.login) {
        const chunks = req.cookies.login.split(":");
        if (chunks.length === 2 && accounts.has(chunks[0]) && accounts.get(chunks[0]).password === chunks[1]) {
            res.locals.user = chunks[0];
        }
    }
    next();
});

// templating engines are for losers!
const postTemplate = fs.readFileSync(path.join(__dirname, "post.html"), "utf8");
app.get("/post/:id", (req, res) => {
    if (posts.has(req.params.id)) {
        res.type("text/html").send(postTemplate.replace("$CONTENT", () => posts.get(req.params.id)));
    } else {
        res.status(400).type("text/html").send(postTemplate.replace("$CONTENT", "post not found :("));
    }
});

app.get("/", needsAuth);
app.get("/login", (req, res, next) => {
    if (res.locals.user) {
        res.redirect("/");
    } else {
        next();
    }
});
app.use(express.static(path.join(__dirname, "static"), { extensions: ["html"] }));

app.post("/register", (req, res) => {
    if (typeof req.body.username !== "string" || typeof req.body.password !== "string" || typeof req.body.displayName !== "string") {
        res.redirect("/login#" + encodeURIComponent("Please metafill out all the metafields."));
        return;
    }
    const username = req.body.username.trim();
    const password = req.body.password.trim();
    const displayName = req.body.displayName.trim();
    if (!/^[\w]{3,32}$/.test(username) || !/^[-\w !@#$%^&*()+]{3,32}$/.test(password) || !/^[-\w ]{3,64}/.test(displayName)) {
        res.redirect("/login#" + encodeURIComponent("Invalid metavalues provided for metafields."));
        return;
    }
    if (accounts.has(username)) {
        res.redirect("/login#" + encodeURIComponent("Metaaccount already metaexists."));
        return;
    }
    accounts.set(username, { password, displayName, posts: [], friends: [] });
    cleanup.push([username, Date.now() + 1000 * 60 * 60 * 12]);
    res.cookie("login", `${username}:${password}`, { httpOnly: true });
    res.redirect("/");
});

app.post("/login", (req, res) => {
    if (typeof req.body.username !== "string" || typeof req.body.password !== "string") {
        res.redirect("/login#" + encodeURIComponent("Please metafill out all the metafields."));
        return;
    }
    const username = req.body.username.trim();
    const password = req.body.password.trim();
    if (accounts.has(username) && accounts.get(username).password === password) {
        res.cookie("login", `${username}:${password}`, { httpOnly: true });
        res.redirect("/");
    } else {
        res.redirect("/login#" + encodeURIComponent("Wrong metausername/metapassword."));
    }
});

app.post("/friend", needsAuth, (req, res) => {
    res.type("text/plain");
    const username = req.body.username.trim();
    if (!accounts.has(username)) {
        res.status(400).send("Metauser doesn't metaexist");
    } else {
        const user = accounts.get(username);
        if (user.friends.includes(res.locals.user)) {
            res.status(400).send("Already metafriended");
        } else {
            user.friends.push(res.locals.user);
            res.status(200).send("ok");
        }
    }
});

app.post("/post", needsAuth, (req, res) => {
    res.type("text/plain");
    const id = uuid();
    const content = req.body.content;
    if (typeof content !== "string" || content.length > 1000 || content.length === 0) {
        res.status(400).send("Invalid metacontent");
    } else {
        const user = accounts.get(res.locals.user);
        posts.set(id, content);
        user.posts.push(id);
        res.send(id);
    }
});

app.get("/posts", needsAuth, (req, res) => {
    res.type("application/json");
    res.send(
        JSON.stringify(
            accounts.get(res.locals.user).posts.map((id) => {
                const content = posts.get(id);
                return {
                    id,
                    blurb: content.length < 50 ? content : content.slice(0, 50) + "...",
                };
            })
        )
    );
});

app.get("/friends", needsAuth, (req, res) => {
    res.type("application/json");
    res.send(
        JSON.stringify(
            accounts
                .get(res.locals.user)
                .friends.filter((username) => accounts.has(username))
                .map((username) => ({
                    username,
                    displayName: accounts.get(username).displayName,
                }))
        )
    );
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
