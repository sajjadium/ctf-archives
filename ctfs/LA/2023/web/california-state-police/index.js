const express = require("express");
const path = require("path");
const { v4: uuid } = require("uuid");
const cookieParser = require("cookie-parser");

const flag = process.env.FLAG;
const port = parseInt(process.env.PORT) || 8080;
const adminpw = process.env.ADMINPW || "placeholder";

const app = express();

const reports = new Map();

let cleanup = [];

setInterval(() => {
    const now = Date.now();
    let i = cleanup.findIndex(x => now < x[1]);
    if (i === -1) {
        i = cleanup.length;
    }
    for (let j = 0; j < i; j ++) {
        reports.delete(cleanup[j][0]);
    }
    cleanup = cleanup.slice(i);
}, 1000 * 60);

app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));

app.get("/flag", (req, res) => {
    res.status(400).send("you have to POST the flag this time >:)");
});

app.post("/flag", (req, res) => {
    if (req.cookies.adminpw === adminpw) {
        res.send(flag);
    } else {
        res.status(400).send("no hacking allowed");
    }
});

app.use((req, res, next) => {
    res.set(
        "Content-Security-Policy",
        "default-src 'none'; script-src 'unsafe-inline'"
    );
    next();
});

app.post("/report", (req, res) => {
    res.type("text/plain");
    const crime = req.body.crime;
    if (typeof crime !== "string") {
        res.status(400).send("no crime provided");
        return;
    }
    if (crime.length > 2048) {
        res.status(400).send("our servers aren't good enough to handle that");
        return;
    }
    const id = uuid();
    reports.set(id, crime);
    cleanup.push([id, Date.now() + 1000 * 60 * 60 * 3]);
    res.redirect("/report/" + id);
});

app.get("/report/:id", (req, res) => {
    if (reports.has(req.params.id)) {
        res.type("text/html").send(reports.get(req.params.id));
    } else {
        res.type("text/plain").status(400).send("report doesn't exist");
    }
});

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
