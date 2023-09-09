const express = require("express");
const https = require("https");
const puppeteer = require("puppeteer");
const fs = require('fs');

const bot = express();

const port = process.env.PORT || 443;
const APP_HOST = process.env.APP_HOST || "localhost";
const BOT_HOST = process.env.BOT_HOST || "bot.internal";
const SCOREBOARD_URL = process.env.SCOREBOARD_URL || "http://ctf2023.hitcon.org";
const FLAG = process.env.FLAG || "hitcon{test_flag}";

let browser = null;

const rateLimit = new Map();

bot.use((req, res, next) => {
    if (req.hostname !== BOT_HOST) {
        return res.status(403).send("Forbidden");
    }
    next();
});

bot.get("/visit", async (req, res) => {
    const { path, token } = req.query;
    if (!path || !token) {
        return res.status(400).send("Missing path or token");
    }
    if (!token.match(/^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$/)) {
        return res.status(400).send('Token is not a valid uuid');
    }

    let id;
    try {
        id = (await fetch(
            `${SCOREBOARD_URL}/team/token_auth?token=${token}`,
            { headers: { Host: 'ctf2023.hitcon.org' } }
        ).then((res) => res.json())).id;
    } catch (e) {
        return res.status(500).send("Error verifying token (maybe scoreboard is down?)");
    }

    if (!id) {
        return res.status(400).send("Invalid token");
    }

    // 10 visits per 1 minute
    const now = Date.now();
    if (rateLimit.has(id)) {
        const [lastVisit, count] = rateLimit.get(id);
        if (now - lastVisit < 60 * 1000) {
            if (count >= 10) {
                return res.status(429).send("Too many requests");
            }
            rateLimit.set(id, [now, count + 1]);
        } else {
            rateLimit.set(id, [now, 1]);
        }
    } else {
        rateLimit.set(id, [now, 1]);
    }

    // === start visiting ===

    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();
    page.setCookie({
        name: "FLAG",
        value: FLAG,
        domain: BOT_HOST,
        path: "/flag",
        secure: true,
        sameSite: "Strict",
    });

    const url = `https://${APP_HOST}${path}`;
    console.log(`[+] Visiting ${url}`);
    try {
        await page.goto(url, { waitUntil: "networkidle0" });
        res.status(200).send("OK");
    } catch (e) {
        console.error(`[+] error visting ${path}`, e);
        res.status(500).send("Something went wrong");
    }
    await page.close();
    await context.close();
});



https.createServer({
    key: fs.readFileSync('/opt/certificates/privkey.pem'),
    cert: fs.readFileSync('/opt/certificates/fullchain.pem')
}, bot).listen(port, async () => {
    browser = await puppeteer.launch({
        pipe: true,
        dumpio: true,
        args: [
            "--js-flags=--jitless,--no-expose-wasm",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ],
        headless: "new",
    });
    console.log(`Express app listening at https://localhost:${port}`);
});
