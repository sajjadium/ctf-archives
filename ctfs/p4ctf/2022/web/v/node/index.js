const fs = require("fs").promises;
const path = require("path");
const Koa = require('koa');
const Router = require('koa-router');
const { koaBody } = require('koa-body');
const crypto = require("crypto");
const logger = require('koa-logger');
const render = require("koa-ejs");
const net = require('net');

const XSSBOT_DOMAIN = process.env.XSSBOT_DOMAIN || 'bot';
const XSSBOT_PORT = process.env.XSSBOT_PORT || 1338;
const FLAG = process.env.FLAG || "FLAG{WIN}";

const router = new Router();
const app = new Koa();
app.use(logger());

app.use(async (ctx, next) => {
    await next();
    ctx.headers['Cache-control'] = 'public, max-age=300';
    ctx.headers['X-Frame-Options'] = 'DENY';
    ctx.headers['X-Content-Type-Options'] = 'nosniff';
});

render(app, {
    root: path.join(__dirname, "templates"),
    layout: "template",
    viewExt: "html",
    cache: false,
});

router.post('/upload', koaBody({
    multipart: true,
    urlencoded: true,
    uploadDir: '/tmp',
}), async ctx => {
    try {
        const keys = Object.keys(ctx.request.files);
        if (keys.length != 1)
        {
            ctx.body = "plz gib 1 file";
        }
        else
        {
            const key = keys[0];
            const entry = ctx.request.files[key];
            const extension = entry.originalFilename.split(".").pop();
            if (extension.includes(".."))
                throw -1;
            if (extension.includes("/"))
                throw -1;
            const name = `${crypto.randomUUID()}.${extension}`;
            await fs.copyFile(entry.filepath, `/files/${name}`);
            ctx.body = name;
        }
    } catch(err) {
        console.log(`error ${err.message}`);
        ctx.body = err.message;
    }
})

router.get('/upload', async (ctx, next) => {
    await ctx.render("upload");
});

router.get('/', async (ctx, next) => {
    await ctx.render("root");
});

router.get('/login', async (ctx, next) => {
    await ctx.render("login");
});

router.post('/login', koaBody({
    multipart: true,
    urlencoded: true,
}), async (ctx, next) => {
    try
    {
        if (ctx.request.body.username !== process.env.BOT_USER)
            throw -1;

        if (ctx.request.body.password !== process.env.BOT_PASS)
            throw -1;

        // chosen by a fair openssl-roll
        ctx.cookies.set('cryptosecretsession', 'aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1RSDItVEdVbHd1NAo=', { secure: false });
        await ctx.render("flag", {"flag": FLAG});
    } catch(err) {
        console.log(err);
        // chosen by a fair rick-roll
        ctx.redirect("https://www.youtube.com/watch?v=86IqIUtKQXY");
    }
});

router.get('/report', async (ctx, next) => {
    await ctx.render('report');
});

router.post('/report', koaBody({
    multipart: true,
    urlencoded: true,
}), async (ctx, next) => {
    const url = ctx.request.body.url;
    if (typeof url !== 'string') {
        ctx.body = "Invalid type for URL";
        return next();
    }

    if (url.length > 256) {
        ctx.body = "Too long URL!";
        return next();
    }

    if (!/^https?:\/\//.test(url)) {
        ctx.body = "The URL needs to start with https?://";
        return next();
    }

    const timeout = 15000;
    const client = net.Socket();
    client.connect(XSSBOT_PORT, XSSBOT_DOMAIN);
    await new Promise(resolve => {
        let scheduled = false;
        client.on('data', data => {
            let msg = data.toString();
            if (msg.includes("Please send me")) {
                client.write(JSON.stringify({
                    url,
                    timeout
                }) + '\n');
                console.log(`sending to bot: ${url}`);
            }
            if(msg.includes("position in the queue")){
                scheduled = true;
                ctx.body = msg;
                client.destroy();
                resolve(1);
            }
        });

        setTimeout(()=>{
            if(!scheduled){
                ctx.body = "Something wrong with the bot, please reach out to admins.";
                console.error("Bot is not responsive.");
                resolve(-1);
            }
        }, 5000);
    });
});

app.use(router.routes());
app.listen(4000);
console.log("listening on port 4000");

// start cleaning loop
setTimeout(async () => {
    console.log("start cleanup");
    try {
        const files = await fs.readdir("/files");
        for (const file of files) {
            if (file.length > 10)
                await fs.unlink(path.resolve("/files", file));
        }
    } catch (err){
        console.log(err);
    }
    console.log("done");
}, 1000 * 60 * 15);
