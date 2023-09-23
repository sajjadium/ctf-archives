import { randomUUID } from "crypto";
import express from "express";
import DOMPurify from "isomorphic-dompurify";
import path, { dirname } from "path";
import { fileURLToPath } from "url";
import { firefox } from "playwright";
import he from "he";
import { setTimeout } from "timers/promises";

const app = express();
const PORT = process.env.PORT || 1337;

app.set("view engine", "ejs");
app.set("views", path.join(dirname(fileURLToPath(import.meta.url)), "views"));

app.use(express.urlencoded({ extended: true }));

const notesByUUID = {};
const ipToUUID = {};

app.get("/", (req, res) => {
    const ipAddress = req.ip;
    let user = ipToUUID[ipAddress];

    if (!user) {
        user = randomUUID();
        ipToUUID[ipAddress] = user;
        notesByUUID[user] = [];
    }

    res.render("index", {
        user: user,
        notes: notesByUUID[user]
    });
});

app.post("/add_note", (req, res) => {
    const ipAddress = req.ip;
    const user = ipToUUID[ipAddress];
    const noteContent = he.encode(DOMPurify.sanitize(he.decode(req.body.note)));

    if (noteContent) {
        notesByUUID[user].push(noteContent);
    }

    res.redirect("/");
});

app.get("/delete_note/:noteId", (req, res) => {
    const ipAddress = req.ip;
    const user = ipToUUID[ipAddress];
    const noteId = parseInt(req.params.noteId, 10);

    if (noteId >= 0 && noteId < notesByUUID[user].length) {
        notesByUUID[user].splice(noteId, 1);
    }

    res.redirect("/");
});

app.get("/raw/:user", (req, res) => {
    const userNotes = (notesByUUID[req.params.user] || []).join("\n");
    res.setHeader("content-type", "text/plain");
    res.send(userNotes);
});

app.get("/view/", (req, res) => {
    res.render("view", {
        user: req.query.user,
    });
});

app.get("/report", async (req, res) => {
    try {
        if (new URL(req.query.url).host !== "flarenotes.vsc.tf") {
            return res.send("wtf is this lmao");
        }
    } catch (e) {
        return res.send("invalid url");
    }

    const browser = await firefox.launch();
    const context = await browser.newContext();

    const page = await context.newPage();
    await page.goto(`https://flarenotes.vsc.tf/`);

    await context.addCookies([
        {
            name: "flag",
            value: process.env.FLAG || "vsctf{fake_flag}",
            domain: "flarenotes.vsc.tf",
            path: "/",
        },
    ]);

    await page.goto(req.query.url, { waitUntil: "domcontentloaded" });
    await setTimeout(10000);
    await context.close();

    res.send("successfully reported!");
});

app.listen(PORT, "::", () => {
    console.log(`Server started on port ${PORT}`);
});
