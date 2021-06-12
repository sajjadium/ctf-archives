import Koa from 'koa';
import koaStatic from 'koa-static';
import Router from '@koa/router';
import jwt from 'jsonwebtoken';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import bodyParser from 'koa-bodyparser';
import send from 'koa-send';

const __dirname = dirname(fileURLToPath(import.meta.url));

let yesVotes = 0;
let noVotes = 0;

const privateKey = readFileSync(join(__dirname, "key.priv"), "utf8");
const publicKey = readFileSync(join(__dirname, "key"), "utf8");
const msgs = readFileSync(join(__dirname, "errormessages"), "utf8").split("\n").filter(s => s.length > 0);
/** @type {import("./languages.json")} */
const languages = JSON.parse(readFileSync(join(__dirname, "languages.json"), "utf8"));

const languageRegex = /^[a-z]+$/;

const app = new Koa();
const router = new Router();

/**
 * @param {string} language
 * @returns {string}
 */
function generateToken(language) {
    return jwt.sign({ language }, privateKey, { algorithm: "RS256" });
}

router.get("/localisation-file", async ctx => {
    const token = ctx.cookies.get("lion-token");
    /** @type {string} */
    let language;
    if (token) {
        const payload = await new Promise((resolve, reject) => {
            try {
                jwt.verify(token, publicKey, (err, result) => err ? reject(err) : resolve(result));
            } catch (e) {
                reject(e);
            }
        });
        language = payload.language;
    } else {
        language = languages[Math.floor(Math.random() * languages.length)].id;
        ctx.cookies.set("lion-token", generateToken(language));
    }
    await send(ctx, language, {root: __dirname});
});

router.post("/localization-language", async ctx => {
    const language = ctx.request.body?.language;
    if (typeof language === "string") {
        if (language.match(languageRegex)) {
            ctx.cookies.set("lion-token", generateToken(language));
        } else {
            ctx.throw(400, msgs[Math.floor(Math.random() * msgs.length)]);
        }
    } else {
        ctx.throw(400, "no language");
    }
    ctx.redirect("/");
});

router.get("/languages", async ctx => {
    ctx.body = languages;
});

router.post("/y", async ctx => {
    yesVotes++;
    ctx.body = [yesVotes, noVotes];
});

router.post("/n", async ctx => {
    noVotes++;
    ctx.body = [yesVotes, noVotes];
});

app.use(bodyParser());
app.use(router.routes());
app.use(router.allowedMethods());
app.use(koaStatic(join(__dirname, "../public")));
app.listen(1337);