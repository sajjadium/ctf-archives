import express from 'express';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';
import Datastore from 'nedb';
import puppeteer from 'puppeteer';
import { randomFillSync } from 'crypto';
import { readFileSync } from 'fs';
import cookieParser from 'cookie-parser';

const __dirname = dirname(fileURLToPath(import.meta.url));

const db = new Datastore();
db.ensureIndex({
    fieldName: "created",
    expireAfterSeconds: 10 * 60
}, () => {})

const browser = puppeteer.launch({args: ["--incognito", "--no-sandbox"]});

const secret = randomFillSync(Buffer.alloc(60)).toString("base64");
console.log(`Secret: ${secret}`);
const flag = readFileSync(join(__dirname, "flag.txt"), "utf8");

const app = express();
app.use(express.json({
    type: ["application/json", "application/csp-report"]
}));
app.use(cookieParser());

app.post("/visit", async (req, res) => {
    try {
        if (typeof req.body !== "object" || typeof req.body.id !== "string") return res.status(400).send("id must be a string");
        const context = await (await browser).createIncognitoBrowserContext();
        const page = await context.newPage();
        await page.setCookie({
            name: "secret",
            value: secret,
            domain: "localhost"
        });
        await page.goto("http://localhost:1337/page/" + encodeURIComponent(req.body.id), {waitUntil: "networkidle0", timeout: 3000});
        await page.close();
        await context.close();
        res.json({visited: true});
    } catch (e) {
        console.error(e);
        res.status(500);
        res.json({error: true});
    }
});

app.post("/publish", (req, res) => {
    db.insert({...req.body, created: new Date(), cspViolations: 0, cspChars: 0}, (error, page) => {
        if (error) {
            console.error(error);
            res.status(500);
            res.json({error: true});
        } else {
            res.json({id: page._id});
        }
    });
});

app.post("/report-csp-violation", (req, res) => {
    if (!req.query || typeof req.query.id !== "string") return res.status(400).send("id must be a string");
    if (typeof req.body !== "object" || typeof req.body["csp-report"] !== "object") return res.status(400).send("not a csp report");
    db.update({_id: req.query.id}, {$inc: {cspViolations: 1, cspChars: req.body["csp-report"]["script-sample"]?.length || 0}}, {}, (error, count, _) => {
        if (error) {
            console.error(error);
            res.sendStatus(500);
        } else if (count > 0) {
            res.sendStatus(200);
        } else {
            res.sendStatus(404);
        }
    });
});

app.get("/page/:id", (req, res) => {
    db.findOne({_id: req.params.id}, (error, page) => {
        if (error) {
            console.error(error);
            res.sendStatus(500);
        } else if (page) {
            res.type("html");
            const violationContent = page.cspViolations > 0 ? `<p>Our Completely Secure Publishing system has blocked <strong>${page.cspViolations}</strong> hacking attempt${page.cspViolations === 1 ? "" : "s"} on this page${page.cspChars > 0 ? ` totalling ${page.cspChars}+ characters` : ""}.</p>` : "";
            const adminContent = req.cookies.secret === secret ? `<p>Prize: ${flag}</p>` : "<p>You must be an administrator to judge the writing competition.</p>";
            const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${page.title || "Untitled"}</title></head><body>${violationContent}${page.content || ""}${adminContent}</body></html>`;
            res.set("Content-Security-Policy", `child-src 'none'; connect-src 'none'; default-src 'none'; font-src 'none'; frame-src 'none'; img-src 'none'; manifest-src 'none'; media-src 'none'; object-src 'none'; prefetch-src 'none'; script-src 'report-sample'; style-src 'report-sample'; worker-src 'none'; report-uri /report-csp-violation?id=${req.params.id}`);
            res.type("html");
            res.send(html);
        } else {
            res.sendStatus(404);
        }
    });
});

app.use(express.static(join(__dirname, "../public")));

app.listen(1337);
console.log("Listening on http://localhost:1337");