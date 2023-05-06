const express = require("express");
const crypto = require("crypto");

const app = express();

const PORT = process.env.PORT || 8080;

app.set('view engine', 'hbs');

app.use(require("cookie-parser")());
app.use(express.static("public"));

app.use((req, res, next) => {
    res.setHeader("Cache-Control", "no-cache, no-store");
    res.setHeader("Content-Security-Policy",
        "default-src 'self'; object-src 'none'; base-uri 'none'; script-src * 'unsafe-inline';" // ;^)
    );

    if(!req.cookies["__Host-token"]) {
        res.cookie("__Host-token", crypto.randomBytes(32).toString("hex"), { secure: true });
    }

    try {
        app.locals.results = JSON.parse(req.cookies?.["__Host-results"]);
    }
    catch(err) {
        app.locals.results = [
            "enter your expression above, and press \"calculate\" to see the value here!"
        ];
        res.cookie("__Host-results", JSON.stringify(app.locals.results), { secure: true });
    }

    next();
});

app.get("/", (req, res) => res.render("home"));
app.get("/calc", (req, res) => res.render("calc"));

app.listen(PORT, () => console.log(`web/obligatory-calc listening on port ${PORT}`));