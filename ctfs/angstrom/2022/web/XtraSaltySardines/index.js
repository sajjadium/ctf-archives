const express = require("express");
const path = require("path");
const fs = require("fs");
const cookieParser = require("cookie-parser");

const app = express();
const port = Number(process.env.PORT) || 8080;
const sardines = {};

const alpha = "abcdefghijklmnopqrstuvwxyz";

const secret = process.env.ADMIN_SECRET || "secretpw";
const flag = process.env.FLAG || "actf{placeholder_flag}";

function genId() {
    let ret = "";
    for (let i = 0; i < 10; i++) {
        ret += alpha[Math.floor(Math.random() * alpha.length)];
    }
    return ret;
}

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

// the admin bot will be able to access this
app.get("/flag", (req, res) => {
    if (req.cookies.secret === secret) {
        res.send(flag);
    } else {
        res.send("you can't view this >:(");
    }
});

app.post("/mksardine", (req, res) => {
    if (!req.body.name) {
        res.status(400).type("text/plain").send("please include a name");
        return;
    }
    // no pesky chars allowed
    const name = req.body.name
        .replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
        .replace("<", "&lt;")
        .replace(">", "&gt;");
    if (name.length === 0 || name.length > 2048) {
        res.status(400)
            .type("text/plain")
            .send("sardine name must be 1-2048 chars");
        return;
    }
    const id = genId();
    sardines[id] = name;
    res.redirect("/sardines/" + id);
});

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});


app.get("/sardines/:sardine", (req, res) => {
    const name = sardines[req.params.sardine];
    if (!name) {
        res.status(404).type("text/plain").send("sardine not found :(");
        return;
    }
    const sardine = fs
        .readFileSync(path.join(__dirname, "sardine.html"), "utf8")
        .replaceAll("$NAME", name.replaceAll("$", "$$$$"));
    res.type("text/html").send(sardine);
});

app.listen(port, () => {
    console.log(`Server listening on port ${port}.`);
});
