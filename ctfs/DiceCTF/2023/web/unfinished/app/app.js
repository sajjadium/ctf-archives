const { MongoClient } = require("mongodb");
const cp = require('child_process');
const express = require("express");

const client = new MongoClient("mongodb://mongodb:27017/");
const app = express();

const PORT = process.env.PORT || 4444;

app.use(express.urlencoded({ extended: false }));
app.use(require("express-session")({
    secret: require("crypto").randomBytes(32).toString("hex"),
    resave: false,
    saveUninitialized: false
}));

/*
// TODO: add register functionality
app.post("/api/register", (req, res) => {

});
*/

const requiresLogin = (req, res, next) => {
    if (!req.session.user) {
        res.redirect("/?error=You need to be logged in");
    }
    next();
};

app.post("/api/login", async (req, res) => {
    let { user, pass } = req.body;
    if (!user || !pass || typeof user !== "string" || typeof pass !== "string") {
        return res.redirect("/?error=Missing username or password");
    }

    const users = client.db("app").collection("users");
    if (await users.findOne({ user, pass })) {
        req.session.user = user;
        return res.redirect("/");
    }
    res.redirect("/?error=Invalid username or password");
});

app.post("/api/ping", requiresLogin, (req, res) => {
    let { url } = req.body;
    if (!url || typeof url !== "string") {
        return res.json({ success: false, message: "Invalid URL" });
    }

    try {
        let parsed = new URL(url);
        if (!["http:", "https:"].includes(parsed.protocol)) throw new Error("Invalid URL");
    }
    catch (e) {
        return res.json({ success: false, message: e.message });
    }

    const args = [ url ];
    let { opt, data } = req.body;
    if (opt && data && typeof opt === "string" && typeof data === "string") {
        if (!/^-[A-Za-z]$/.test(opt)) {
            return res.json({ success: false, message: "Invalid option" });
        }

        // if -d option or if GET / POST switch
        if (opt === "-d" || ["GET", "POST"].includes(data)) {
            args.push(opt, data);
        }
    }

    cp.spawn('curl', args, { timeout: 2000, cwd: "/tmp" }).on('close', (code) => {
        // TODO: save result to database
        res.json({ success: true, message: `The site is ${code === 0 ? 'up' : 'down'}` });
    });
});

app.get("/", (req, res) => res.sendFile(req.session.user ? "dashboard.html" : "index.html", { root: "static" }));

client.connect().then(() => {
    app.listen(PORT, () => console.log(`web/unfinished listening on http://localhost:${PORT}`));
});