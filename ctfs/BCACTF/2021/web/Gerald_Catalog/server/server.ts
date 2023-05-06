import Router from '@koa/router';
import Koa, { ParameterizedContext } from 'koa';
import send from 'koa-send';
import { generateGerald } from './image';
import koaStatic from 'koa-static';
import { readFileSync } from 'fs';
import { readFile } from 'fs/promises';
import { DB } from './database';
import bodyParser from 'koa-bodyparser';
import { compile } from 'handlebars';
import { sendNotifications, validateSubscription } from './notify';
import { randomBytes } from 'crypto';
import session from 'koa-session';
import passport from 'koa-passport';
import { Strategy as LocalStrategy } from 'passport-local';

const maxCaptionLength = 100;
const secretKey = randomBytes(16).toString("base64");

const app = new Koa();
const db = new DB(readFileSync("flag.txt", "utf8"));
const router = new Router();

const templates: Record<string, HandlebarsTemplateDelegate<any>> = {};
async function render(ctx: ParameterizedContext<any, any, any>, template: string, input?: any) {
    if (process.env.NODE_ENV !== "PRODUCTION" || !templates[template]) {
        templates[template] = compile(await readFile(template, "utf8"));
    }
    ctx.body = templates[template](input);
}

passport.use(new LocalStrategy((username, password, done) => {
    if (db.authenticate(username, password)) {
        done(null, username);
    } else {
        done(null, false, {message: "Incorrect username or password."});
    }
}));

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((id, done) => done(null, id as string));

router.get("/", async (ctx) => {
    await render(ctx, "index.hbs");
});

router.get("/login", async ctx => {
    await render(ctx, "login.hbs", {
        flash: ctx.session!.flash
    });
});

router.post("/login", passport.authenticate("local", {
    successRedirect: "/geralds",
    failureRedirect: "/login",
    failureFlash: "Incorrect username or password."
}));

router.get("/register", async ctx => {
    await render(ctx, "register.hbs");
});

router.post("/register", async ctx => {
    const username: unknown = ctx.request.body.username;
    const password: unknown = ctx.request.body.password;

    if (typeof username !== "string") {
        ctx.throw(400, "username must be a string");
        return;
    }

    if (typeof password !== "string") {
        ctx.throw(400, "password must be a string");
        return;
    }

    if (username.length < 3 || username.length > 20) {
        ctx.throw(400, "username must be 3 to 20 characters");
    }

    if (password.length < 8) {
        ctx.throw(400, "password must be at least 8 characters");
    }

    if (!db.createUser(username, password)) {
        ctx.throw(400, "username taken");
    }

    // @ts-ignore
    ctx.login(username);
    ctx.redirect("/geralds");
});

router.get("/logout", async ctx => {
    // @ts-ignore
    ctx.logout();
    ctx.redirect("/login");
});

router.get("/geralds", async ctx => {
    if (!ctx.state.user) {
        ctx.redirect("/login");
        return;
    }

    await render(ctx, "geralds.hbs", {
        geralds: db.getGeralds(ctx.state.user),
        username: ctx.state.user
    });
});

router.get("/gerald/:id", async (ctx) => {
    const id: string = ctx.params.id;
    const gerald = db.getGerald(id);
    if (gerald) {
        if (gerald.copyrightClaim && ctx.ip !== "127.0.0.1" && ctx.ip !== "::1" && ctx.ip !== "::ffff:127.0.0.1") {
            ctx.throw(451, "Geralds with active copyright claims can only be viewed by an on-site administrator.");
        } else {
            await sendNotifications(id, gerald);
            await render(ctx, "gerald.hbs", {
                gerald,
                image: gerald.caption ? `/gerald.png?caption=${encodeURIComponent(gerald.caption)}` : "/gerald.png"
            });
        }
    }
});

router.get("/gerald.png", async (ctx) => {
    const caption = ctx.query.caption;
    if (typeof caption === "string" && caption.trim().length > 0) {
        if (caption.length >= maxCaptionLength) {
            ctx.throw(400, "caption is too long");
        }
        const stream = await generateGerald(caption);
        ctx.type = "image/png";
        ctx.body = stream;
    } else {
        await send(ctx, "gerald.PNG");
    }
});

router.get("/add", async ctx => {
    await render(ctx, "add.hbs", {
        username: ctx.state.user,
        maxLength: maxCaptionLength
    });
});

router.post("/add", async ctx => {
    if (!ctx.state.user) {
        ctx.throw(401, "not logged in");
        return;
    }

    const name: unknown = ctx.request.body.name;
    const caption: unknown = ctx.request.body.caption;

    if (typeof name !== "string") {
        ctx.throw(400, "name must be a string");
        return;
    }

    if (typeof caption !== "string" && typeof caption !== "undefined") {
        ctx.throw(400, "caption must be a string");
        return;
    }

    if (caption && caption.length > maxCaptionLength) {
        ctx.throw(400, "caption is too long");
    }

    const id = db.addGerald({name, caption}, ctx.state.user);
    if (!id) {
        ctx.throw(500, "an error occurred");
        return;
    }

    ctx.redirect(`/geralds`);
});

router.put("/gerald/:id/subscription", async ctx => {
    if (!ctx.state.user) {
        ctx.throw(401, "not logged in");
        return;
    }

    const id: string = ctx.params.id;
    if (!db.getGerald(id)) return;
    if (!db.ownsGerald(ctx.state.user, id)) {
        ctx.throw(403, "this gerald is not your gerald");
        return;
    }

    const subscription = validateSubscription(ctx.request.body);
    if (!subscription) {
        ctx.throw(400, "invalid subscription");
        return;
    }

    db.setSubscription(id, subscription);
    ctx.body = "ok";
});

router.delete("/gerald/:id/subscription", async ctx => {
    if (!ctx.state.user) {
        ctx.throw(401, "not logged in");
        return;
    }

    const id: string = ctx.params.id;
    if (!db.getGerald(id)) return;
    if (!db.ownsGerald(ctx.state.user, id)) {
        ctx.throw(403, "this gerald is not your gerald");
    }
    
    db.setSubscription(id, undefined);
    ctx.body = "ok";
});

app.keys = [secretKey];

app.use(bodyParser());
app.use(session({}, app));
app.use(async (ctx, next) => {
    let didUpdateFlash = false;
    try {
        ctx.flash = (type: any, message: any) => {
            ctx.session!.flash = { type, message };
            didUpdateFlash = true;
        };
        await next();
    } finally {
        if (ctx.session!.flash && !didUpdateFlash) {
            delete ctx.session!.flash;
        }
    }
});
app.use(passport.initialize());
app.use(passport.session());
app.use(router.routes());
app.use(koaStatic("../public"));

app.listen(1337);
console.log("Listening at http://localhost:1337");
