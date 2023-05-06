const express = require("express");
const crypto = require("crypto");

const app = express();

const PORT = process.env.PORT || 8080;

const sha256 = (data) => crypto.createHash("sha256").update(data).digest("hex");

const users = new Map();
const posts = new Map();

(() => {
    const flagId = crypto.randomBytes(6).toString("hex");
    const flag = process.env.FLAG || "flag{test_flag}";
    users.set("admin", {
        pass: sha256(process.env.ADMIN_PASSWORD || "test_password"),
        posts: Object.freeze([flagId]),
    });
    posts.set(flagId, {
        id: flagId,
        title: "Flag",
        body: flag,
    });
})();

const session = require("express-session");
const MemoryStore = require("memorystore")(session)

app.use(
    session({
        cookie: { maxAge: 3600000 },
        store: new MemoryStore({
            checkPeriod: 3600000, // prune expired entries every 1h
        }),
        resave: false,
        saveUninitialized: false,
        secret: crypto.randomBytes(32).toString("hex"),
    })
);

app.use(express.json());

app.use((req, res, next) => {
    res.setHeader(
        "Content-Security-Policy",
        "script-src 'self'; object-src 'none'; base-uri 'none';"
    );
    if (req.session.user && users.has(req.session.user)) {
        req.user = users.get(req.session.user);
    }
    next();
});

app.use(express.static("public"));

app.post("/api/login", (req, res) => {
    let { user, pass } = req.body;
    if (
        !user ||
        !pass ||
        typeof user !== "string" ||
        typeof pass !== "string"
    ) {
        return res.json({
            success: false,
            error: "Missing username or password",
        });
    }

    if (!users.has(user)) {
        return res.json({
            success: false,
            error: "No user exists with that username",
        });
    }

    if (users.get(user).pass !== sha256(pass)) {
        return res.json({ success: false, error: "Invalid password" });
    }

    req.session.user = user;
    res.json({ success: true });
});

app.post("/api/register", (req, res) => {
    let { user, pass } = req.body;
    if (
        !user ||
        !pass ||
        typeof user !== "string" ||
        typeof pass !== "string"
    ) {
        return res.json({
            success: false,
            error: "Missing username or password",
        });
    }

    if (user.length < 5 || pass.length < 7) {
        return res.json({
            success: false,
            error: "Please choose a longer username or password",
        });
    }

    if (users.has(user)) {
        return res.json({
            success: false,
            error: "A user exists with that username",
        });
    }

    req.session.user = user;
    users.set(user, {
        pass: sha256(pass),
        posts: [],
    });

    res.json({ success: true });
});

const requiresLogin = (req, res, next) =>
    req.user
        ? next()
        : res.json({ success: false, error: "You must be logged in!" });

app.post("/api/create", requiresLogin, (req, res) => {
    if (req.session.user === "admin") {
        return res.json({ success: false, error: "uhhhhh... no" });
    }

    let { title, body } = req.body;
    if (
        !title ||
        !body ||
        typeof title !== "string" ||
        typeof body !== "string"
    ) {
        return res.json({ success: false, error: "Missing title or body" });
    }

    let id = crypto.randomBytes(6).toString("hex");

    posts.set(id, { id, title, body });
    req.user.posts.push(id);

    res.json({ success: true });
});

app.post("/api/posts", requiresLogin, (req, res) => {
    return res.json({
        success: true,
        data: req.user.posts.map((id) => posts.get(id)),
    });
});

app.get("/api/post/:id", requiresLogin, (req, res) => {
    let { id } = req.params;
    if (!id) {
        return res.json({ success: false, error: "No id provided" });
    }
    if (!posts.has(id)) {
        return res.json({
            success: false,
            error: "No post was found with that id",
        });
    }
    return res.json({ success: true, data: posts.get(id) });
});

app.get("*", (req, res) => res.sendFile("index.html", { root: "public" }));

app.listen(PORT, () => console.log(`app listening on port ${PORT}`));
