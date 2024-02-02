const fastify = require("fastify")({ logger: true });
const crypto = require("crypto");
const path = require("path");
const fs = require("fs");

fastify.register(require("@fastify/static"), {
    root: path.join(__dirname, "public")
});
fastify.register(require("@fastify/cookie"));
fastify.register(require("@fastify/formbody"));

const bot = require("./bot");

const templates = {
    "home": fs.readFileSync(`${path.join(__dirname, "templates")}/home.html`).toString(),
    "view": fs.readFileSync(`${path.join(__dirname, "templates")}/view.html`).toString()
};

const notes = new Map();

fastify.addHook('onRequest', (req, reply, done) => {
    // Surely this will be enough to protect my website this time
    // Clueless
    reply.header("Content-Security-Policy", `
        default-src 'self';
        script-src
            'self'
            'sha256-3MXfrskrnUowa38iIoMj9+3kniWYUuDAVNRik0GanAs='
            'sha256-RWw/sDYLoQffrHKbRuya7v6k2wG8+A1eIQPhp9vKO60='
            'unsafe-inline';
        object-src 'none';
        base-uri 'none';
        frame-ancestors 'none';
    `.trim().replace(/\s+/g, " "));
    reply.header("Cache-Control", "no-store");
    reply.header("X-Frame-Options", "DENY");
    reply.header("X-Content-Type-Options", "nosniff");
    reply.header("Referrer-Policy", "no-referrer");
    reply.header("Cross-Origin-Embedder-Policy", "require-corp");
    reply.header("Cross-Origin-Opener-Policy", "same-origin");
    reply.header("Cross-Origin-Resource-Policy", "same-origin");
    reply.header("Document-Policy", "force-load-at-top");

    if (!req.cookies.id) {
        reply.setCookie("id", crypto.randomUUID(), { maxAge: 365 * 24 * 60 * 60, httpOnly: true });
    }

    done();
});

fastify.post("/create", (req, reply) => {
    const { text } = req.body;
    if (!text || typeof text !== "string") {
        return reply.type("text/html").send("Missing text");
    }

    const userNotes = notes.get(req.cookies.id) ?? [];
    const totalLen = userNotes.reduce((prev, curr) => prev + curr.length, 0);

    const newLen = totalLen + text.length;
    if (newLen > 16384) {
        return reply.redirect(`/?message=Cannot add, please delete some notes first (${newLen} > 16384 chars)`);
    }

    userNotes.push(text);
    userNotes.sort();
    notes.set(req.cookies.id, userNotes);

    reply.redirect("/?message=Note added successfully");
});

fastify.post("/remove", (req, reply) => {
    let { index } = req.body;
    if (!index || typeof index !== "string") {
        return reply.redirect("/?message=Missing index");
    }

    index = Number(index);
    if (isNaN(index)) {
        return reply.redirect("/?message=Invalid index");
    }

    const userNotes = notes.get(req.cookies.id) ?? [];
    userNotes.splice(index, 1);

    reply.redirect("/?message=Note removed successfully");
});

fastify.post("/view", (req, reply) => {
    const { viewToken } = req.body;

    if (!req.cookies.viewToken || !viewToken || typeof viewToken !== "string") {
        return reply.redirect("/?message=Missing viewToken");
    }

    if (viewToken !== req.cookies.viewToken) {
        return reply.redirect("/?message=Invalid viewToken");
    }

    const userNotes = notes.get(req.cookies.id) ?? [];
    reply.type("text/html").send(templates.view.replace("{{ notes }}", () => encodeURIComponent(JSON.stringify(userNotes))));
});

let lastVisit = -1;
fastify.post("/submit", (req, reply) => {
    const { url } = req.body;
    if (!url || typeof url !== "string") {
        return reply.redirect("/?message=Missing url");
    }

    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return reply.redirect("/?message=Invalid url");
    }

    const deltaTime = +new Date() - lastVisit;
    if (deltaTime < 30_000) {
        return reply.redirect(`/?message=Please slow down (wait ${(30_000 - deltaTime)/1000} more seconds)`);
    }
    lastVisit = +new Date();

    reply.redirect("/?message=An admin will now look over your submission");
    bot.visit(url);
});

fastify.get("/", (req, reply) => {
    const viewToken = crypto.randomBytes(16).toString("hex");
    reply.setCookie("viewToken", viewToken, { httpOnly: true });
    reply.type("text/html").send(templates.home.replace("{{ viewToken }}", () => viewToken));
});

fastify.listen({ port: 3000, host: '0.0.0.0' }, (err, address) => console.log(err ?? `web/safestlist listening on ${address}`));