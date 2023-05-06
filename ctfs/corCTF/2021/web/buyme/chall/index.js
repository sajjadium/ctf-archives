const express = require("express");
const cookieParser = require("cookie-parser");

const app = express();

require("dotenv").config();

const PORT = process.env.PORT || 80;

app.use(express.static("public"));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.set('view engine', 'hbs');
app.use(cookieParser(process.env.SECRET || require("crypto").randomBytes(32).toString("hex")));

const { flags, users } = require("./db.js");

app.use((req, res, next) => {
    if(req.query.error)
        res.locals.error = req.query.error;
    if(req.query.message)
        res.locals.message = req.query.message;
    if(req.signedCookies.user && users.has(req.signedCookies.user)) {
        let user = users.get(req.signedCookies.user);
        req.user = user;

        let info = {...user};
        info.flags = info.flags.map(f => flags.get(f));
        res.locals.user = info;
    }
    next();
});

app.use("/api", require("./routes/api.js"));
app.get("/flags", (req, res) => res.render("flags", { flags: Object.fromEntries(flags) }));
app.get("/", (req, res) => res.render("index"));

app.listen(PORT, () => {
    console.log(`buyme listening on port ${PORT}`);
});