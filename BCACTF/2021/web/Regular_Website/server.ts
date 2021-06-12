import Router from '@koa/router';
import Koa from 'koa';
import koaStatic from 'koa-static';
import bodyParser from 'koa-bodyparser';
import { launch } from 'puppeteer';
import { readFileSync } from 'fs';

const flag = readFileSync("flag.txt", "utf8");
const verbs = readFileSync("verbs.txt", "utf8").split("\n").map(s => s.trim()).filter(s => {
    return s.length > 0 && !s.startsWith("#");
});

const app = new Koa();
const browser = launch({args: ["--incognito", "--no-sandbox"]});

const router = new Router();
router.post("/", async ctx => {
    if (typeof ctx.request.body !== "object") {
        ctx.throw(400, "body must be an object");
        return;
    }
    const text = ctx.request.body.text;
    if (typeof text !== "string") {
        ctx.throw(400, "text must be a string");
        return;
    }

    const sanitized = text.replace(/<[\s\S]*>/g, "XSS DETECTED!!!!!!");
    const page = await (await browser).newPage();
    await page.setJavaScriptEnabled(true);
    try {
        await page.setContent(`
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Comment</title>
            </head>
            <body>
                <p>Welcome to the Regular Website admin panel.</p>
                <h2>Site Stats</h2>
                <p><strong>Comments:</strong> ???</p>
                <p><strong>Flag:</strong> ${flag}</p>
                <h2>Latest Comment</h2>
                ${sanitized}
            </body>
        </html>
        `, {timeout: 3000, waitUntil: "networkidle2"});
    } catch (e) {
        console.error(e);
        ctx.status = 500;
        ctx.body = "error viewing comment";
        await page.close();
        return;
    }
    ctx.body = `The author of this site has ${verbs[Math.floor(Math.random() * verbs.length)]} your comment.`;
    await page.close();
});

app.use(bodyParser());
app.use(router.routes());
app.use(koaStatic("../public"));
app.listen(1337);
console.log("Listening on port 1337");