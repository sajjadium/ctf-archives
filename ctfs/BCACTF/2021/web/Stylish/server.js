import express from 'express';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import visit from './visit.js';
import generatePasscode from './passcode.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const passcode = generatePasscode();
console.log(`Passcode: ${passcode}`);

const app = express();

app.use(express.urlencoded({extended: false}));

app.get("/flag", (req, res) => {
    if (req.get("X-Passcode") === passcode) {
        res.sendFile(join(__dirname, "flag.txt"));
    } else {
        res.status(403);
        res.type("txt");
        res.send("Incorrect passcode")
    }
});

app.post("/submit", async (req, res) => {
    try {
        const {bg, fg, bbg, bfg} = req.body;
        if (typeof bg !== "string") return res.status(400).type("txt").send("bg must be a string");
        if (typeof fg !== "string") return res.status(400).type("txt").send("fg must be a string");
        if (typeof bbg !== "string") return res.status(400).type("txt").send("bbg must be a string");
        if (typeof bfg !== "string") return res.status(400).type("txt").send("bfg must be a string");
        const encoded = encodeURIComponent(JSON.stringify({ bg, fg, bbg, bfg }));
        if (encoded.length > 2000) return res.status(400).type("txt").send("Theme permalink too long (>2000 chars)");

        await visit(`http://localhost:1337/#${encoded}`, passcode);
        res.type("txt");
        res.send("The admin has checked out your theme!");
    } catch (e) {
        console.error(e.stack);
        res.sendStatus(500);
    }
});

app.use(express.static(join(__dirname, "../public")));

app.listen(1337);
console.log("Listening on http://localhost:1337");