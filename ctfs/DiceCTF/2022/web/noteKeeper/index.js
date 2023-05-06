const express = require("express");
const app = express();

const fsp = require("fs/promises");

const PORT = process.env.PORT || 80;

const utils = require("./src/utils.js");
const db = require("./src/db.js");
const jwt = require("./src/jwt.js");

app.use(express.urlencoded({ extended: false }));
app.use(require('cookie-parser')());
app.use(require('express-jwt')({
    secret: jwt.secret,
    algorithms: ['HS256'],
    credentialsRequired: false,
    getToken: (req) => req.cookies.session
}));

app.use(express.static("public"));
app.use("/api", require("./routes/api.js"));

app.use((req, res, next) => {
    res.setHeader("Content-Security-Policy", `
        script-src 'self';
        object-src 'none';
        frame-src 'none';
        frame-ancestors 'none';
    `.trim().replace(/\s+/g, " "));
    console.log(req.user, req.originalUrl);
    next();
})

app.get("/", (req, res) => {
    res.sendFile("login.html", { root: "pages" });
});

app.get("/home", (req, res) => {
    if(!req.user || !db.hasUser(req.user.username)) return res.redirect("/");
    res.sendFile("home.html", { root: "pages" });
});

app.use((err, req, res, next) => {
    console.log(err);
    utils.alert(req, res, "danger", err.message);
    res.redirect("/home");
});

(async () => {
    // clean up all uploaded files on start
    let files = await fsp.readdir("uploads");
    
    files.filter(f => f !== "flag.mp3").forEach(f => {
        try {
            fsp.rm("uploads/" + f);
        } catch(err) {
            console.log(err);
        }    
    });
})();

app.listen(PORT, () => console.log(`chall listening on port ${PORT}`));
