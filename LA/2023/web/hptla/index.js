const express = require("express");
const path = require("path");
const { v4: uuid } = require("uuid");
const cookieParser = require("cookie-parser");

const flag = process.env.FLAG;
const port = parseInt(process.env.PORT) || 8080;
const adminpw = process.env.ADMINPW || "placeholder";

const app = express();

const lists = new Map();

let cleanup = [];

setInterval(() => {
    const now = Date.now();
    let i = cleanup.findIndex(x => now < x[1]);
    if (i === -1) {
        i = cleanup.length;
    }
    for (let j = 0; j < i; j ++) {
        lists.delete(cleanup[j][0]);
    }
    cleanup = cleanup.slice(i);
}, 1000 * 60);

app.use(cookieParser());
app.use(express.urlencoded({ extended: false }));
app.use((req, res, next) => {
    res.set(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self' 'unsafe-inline'"
    );
    next();
});
app.use(express.static(path.join(__dirname, "static")));

app.post("/list", (req, res) => {
    res.type("text/plain");
    const list = req.body.list;
    if (typeof list !== "string") {
        res.status(400).send("no list provided");
        return;
    }
    const parsed = list
        .trim()
        .split("\n")
        .map((x) => x.trim());
    if (parsed.length > 20) {
        res.status(400).send("list must have at most 20 items");
        return;
    }
    if (parsed.some((x) => x.length > 12)) {
        res.status(400).send("list items must not exceed 12 characters");
        return;
    }
    const id = uuid();
    lists.set(id, parsed);
    cleanup.push([id, Date.now() + 1000 * 60 * 60 * 3]);
    res.send(id);
});

app.get("/list/:id", (req, res) => {
    res.type("application/json");
    if (lists.has(req.params.id)) {
        res.send(lists.get(req.params.id));
    } else {
        res.status(400).send({error: "list doesn't exist"});
    }
});

app.get("/flag", (req, res) => {
    res.type("text/plain");
    if (req.cookies.adminpw === adminpw) {
        res.send(flag);
    } else {
        res.status(401).send("haha no");
    }
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
