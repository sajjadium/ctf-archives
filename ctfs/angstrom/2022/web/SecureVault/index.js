const express = require("express");
const path = require("path");
const fs = require("fs");
const jwt = require("jsonwebtoken");
const cookieParser = require("cookie-parser");

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

// environment config
const port = Number(process.env.PORT) || 8080;
const flag =
    process.env.FLAG ||
    "actf{someone_is_going_to_submit_this_out_of_desperation}";

const userInfo = {};
const jwtKey = Math.random().toString();

class UserStore {
    constructor() {
        this.users = {};
        this.usernames = {};
    }

    insert(username, password) {
        const uid = Math.random().toString();
        this.users[uid] = {
            username,
            uid,
            password,
            vault: "put something here!",
            restricted: true,
        };
        this.usernames[username] = uid;
        return uid;
    }

    get(uid) {
        return this.users[uid] ?? {};
    }

    lookup(username) {
        return this.usernames[username];
    }

    remove(uid) {
        const user = this.get(uid);
        delete this.usernames[user.username];
        delete this.users[uid];
    }
}

function escape(str) {
    return str
        .replaceAll("&", "&amp;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&apos;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
}

const users = new UserStore();

app.use((req, res, next) => {
    try {
        res.locals.user = jwt.verify(req.cookies.token, jwtKey, {
            algorithms: ["HS256"],
        });
    } catch (err) {
        if (req.cookies.token) {
            res.clearCookie("token");
        }
    }
    next();
});

app.get("/", (req, res) => {
    res.type("text/html").send(fs.readFileSync(path.join(__dirname, res.locals.user ? "authed.html" : "index.html"), "utf8"));
});

app.post("/register", (req, res) => {
    if (
        !req.body.username ||
        !req.body.password ||
        req.body.username.length > 32 ||
        req.body.password.length > 32
    ) {
        res.redirect(
            "/?e=" +
                encodeURIComponent("Username and password must be 1-32 chars")
        );
        return;
    }
    if (users.lookup(req.body.username)) {
        res.redirect(
            "/?e=" +
                encodeURIComponent(
                    "Account already exists, please log in instead"
                )
        );
        return;
    }
    const uid = users.insert(req.body.username, req.body.password);
    res.cookie("token", jwt.sign({ uid }, jwtKey, { algorithm: "HS256" }));
    res.redirect("/");
});

app.post("/login", (req, res) => {
    const user = users.get(users.lookup(req.body.username));
    if (user && user.password === req.body.password) {
        res.cookie(
            "token",
            jwt.sign({ uid: user.uid }, jwtKey, { algorithm: "HS256" })
        );
        res.redirect("/");
    } else {
        res.redirect("/?e=" + encodeURIComponent("Invalid username/password"));
    }
});

app.post("/delete", (req, res) => {
    if (res.locals.user) {
        users.remove(res.locals.user.uid);
    }
    res.clearCookie("token");
    res.redirect("/");
});

app.get("/vault", (req, res) => {
    if (!res.locals.user) {
        res.status(401).send("Log in first");
        return;
    }
    const user = users.get(res.locals.user.uid);
    res.type("text/plain").send(user.restricted ? user.vault : flag);
});

app.post("/vault", (req, res) => {
    if (!res.locals.user) {
        res.status(401).send("Log in first");
        return;
    }
    if (!req.body.vault || req.body.vault.length > 2000) {
        res.redirect("/?e=" + encodeURIComponent("Vault must be 1-2000 chars"));
        return;
    }
    users.get(res.locals.user.uid).vault = req.body.vault;
    res.redirect("/");
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
