import express from "express";
import expressSession from "express-session";
import crypto from "crypto";
import hbs from "hbs";

import baseRankings from "./rankings.js";
import calculate from "./ppcalc.js";
import anticheat from "./anticheat.js";

const app = express();
const PORT = process.env.PORT || 4727;

app.use(express.urlencoded({ extended: false, limit: '1mb' }));
app.use(expressSession({
    secret: crypto.randomBytes(32).toString("hex"),
    resave: false,
    saveUninitialized: false
}));
app.set("view engine", "hbs");

hbs.registerHelper('formatNum', v => Math.round(v).toLocaleString());

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const users = new Map();

app.use((req, res, next) => {
    if (req.session.user && users.has(req.session.user)) {
        req.user = users.get(req.session.user);
    }
    res.locals.user = req.user?.username;
    next();
});
const requiresLogin = (req, res, next) => req.user ? next() : res.redirect("/login");

app.post("/api/submit", requiresLogin, async (req, res) => {
    const { osu, osr } = req.body;
    try {
        const [pp, md5] = await calculate(osu, Buffer.from(osr, "base64"));
        if (req.user.playedMaps.includes(md5)) {
            return res.send("You can only submit a map once.");
        }
        if (anticheat(req.user, pp)) {
            // ban!
            users.delete(req.user.username);
            return res.send("You have triggered the anticheat! Nice try...");
        }
        req.user.playCount++;
        req.user.performance += pp;
        req.user.playedMaps.push(md5);
        return res.redirect("/rankings");
    }
    catch (err) {
        return res.send(err.message);
    }
});

app.post("/api/register", (req, res) => {
    const { username, password, flag } = req.body;

    if (!username || typeof username !== "string" || !password || typeof password !== "string") {
        return res.end("missing username or password");
    }
    
    if (username.length < 5 || password.length < 8) {
        return res.end("username or password too short");
    }

    if (users.has(username)) {
        return res.end("a user already exists with that username");
    }

    users.set(username, {
        username,
        password: sha256(password),
        flag: "https://osu.ppy.sh/assets/images/flags/" + (encodeURIComponent(flag) ?? "fallback.png"),
        playCount: 0,
        performance: 0,
        playedMaps: [],
        registerDate: +new Date()
    });

    req.session.user = username;
    res.redirect("/rankings");
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
    res.redirect("/rankings");
});

app.get("/login", (req, res) => res.render("login"));
app.get("/register", (req, res) => res.render("register"));
app.get("/rankings", (req, res) => {
    let ranking = [...baseRankings];

    if (req.user) {
        ranking.push(req.user);
    }

    ranking = ranking
        .sort((a,b) => b.performance - a.performance)
        .map((u, i) => ({ ...u, rank: `#${i + 1}` }));

    let flag;
    if (req.user) {
        if (ranking[ranking.length - 1].username === req.user.username) {
            ranking[ranking.length - 1].rank = "Last";
        }
        else if (ranking[0].username === req.user.username) {
            flag = process.env.FLAG || "osu{test_flag}";
        }
    }

    res.render("rankings", { ranking, flag });
});
app.get("/submit", requiresLogin, (req, res) => res.render("submit"));
app.get("/", (req, res) => res.redirect("/rankings"));

app.listen(PORT, () => console.log(`web/pp-ranking running at http://localhost:${PORT}`));