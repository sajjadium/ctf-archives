const sanitizeFilename = require("sanitize-filename");
const fastify = require('fastify')();
const fsp = require('fs/promises');
const crypto = require('crypto');
const path = require('path');

const bot = require('./bot');

fastify.register(require('@fastify/cookie'));
fastify.register(require('@fastify/session'), {
    secret: crypto.randomBytes(64).toString('hex'),
    cookieName: 'sessionId',
    cookie: { secure: false, maxAge: 365 * 24 * 60 * 60, httpOnly: true }
});
fastify.register(require('@fastify/static'), {
    root: path.join(__dirname, 'public')
});
fastify.setNotFoundHandler((req, res) => {
    res.type("text/html");
    return fsp.readFile(path.join(__dirname, 'public', 'index.html'));
});
fastify.register(require('@fastify/multipart'), {
    limits: {
      fileSize: 64_000,  // For multipart forms, the max file size in bytes
    },
    attachFieldsToBody: true
});

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');

const users = new Map();

fastify.addHook('onRequest', (req, res, done) => {
    if (req.session.get("username") && users.has(req.session.get("username"))) {
        req.user = users.get(req.session.get("username"));
    }
    res.header("Content-Security-Policy", `
        script-src 'sha256-BCut0I6hAnpHxUpwpaDB1crwgr249r2udW3tkBGQLv4=' 'unsafe-inline';
        img-src 'self';
        style-src 'self' 'unsafe-inline' https://fonts.googleapis.com/css2;
        font-src https://fonts.gstatic.com/s/inter/;
        frame-ancestors 'none';
        object-src 'none';
        base-uri 'none';
    `.trim().replace(/\s+/g, " "));
    res.header("Cache-Control", "no-cache, no-store");
    res.header("X-Frame-Options", "DENY");
    done();
});

const requiresLogin = (req, res, done) => req.user ? done() : done(new Error("This action requires authentication"));

fastify.route({
    method: 'GET',
    path: '/api/pastes',
    onRequest: requiresLogin,
    handler: (req, res) => {
        req.user.pastes.forEach(p => p.id = crypto.randomBytes(8).toString("hex"));
        return req.user.pastes.map(({ id, title }) => ({ id, title }));
    }
});

fastify.route({
    method: 'GET',
    path: '/api/paste/:id',
    onRequest: requiresLogin,
    schema: {
        params: {
            type: 'object',
            properties: {
                id: { type: 'string' }
            },
            required: ["id"],
            additionalProperties: false
        }
    },
    handler: (req, res) => {
        const { id } = req.params;
        const paste = req.user.pastes.find(p => p.id === id);

        if (!paste) {
            throw new Error("No paste found with that id");
        }

        req.user.pastes.forEach(p => p.id = crypto.randomBytes(8).toString("hex"));
        return paste;
    }
});

fastify.route({
    method: 'GET',
    path: '/api/destroy/:id',
    onRequest: requiresLogin,
    schema: {
        params: {
            type: 'object',
            properties: {
                id: { type: 'string' }
            },
            required: ["id"],
            additionalProperties: false
        }
    },
    handler: async (req, res) => {
        const { id } = req.params;
        const paste = req.user.pastes.find(p => p.id === id);

        if (!paste) {
            throw new Error("No paste found with that id");
        }

        if (paste.image) {
            try {
                await fsp.rm(path.join(__dirname, 'public', 'uploads', paste.image));
            } catch {}
        }

        req.user.pastes.splice(req.user.pastes.findIndex(p => p.id === id), 1);
        return { success: true };
    }
});

fastify.route({
    method: 'POST',
    path: '/api/create',
    onRequest: requiresLogin,
    handler: async (req, res) => {
        const body = Object.fromEntries(
            Object.keys(req.body).map((key) => [key, req.body[key].value])
        );
        const { title, text } = body;
        
        if (typeof title !== "string" || typeof text !== "string") {
            throw new Error("Title or text must be string");
        }

        if (title.length > 32 || text.length > 512) {
            throw new Error("Title or text too long");
        }

        const id = crypto.randomBytes(8).toString("hex");
        const paste = { id, title, text };

        if (req.body.file) {
            const filename = sanitizeFilename(req.body.file.filename.slice(0, 64), "-");
            const ext = filename.slice(filename.lastIndexOf("."));
            if (![".png", ".jpeg", ".jpg"].includes(ext)) {
                throw new Error("Invalid file format for image");
            }
            const buffer = await req.body.file.toBuffer();
            try {
                await fsp.mkdir(path.join(__dirname, 'public', 'uploads', req.user.user));
            } catch {}
            try {
                await fsp.writeFile(path.join(__dirname, 'public', 'uploads', req.user.user, filename), buffer);
            } catch {}
            paste.image = `${req.user.user}/${filename}`;
        }

        req.user.pastes.push(paste);
        return { success: true };
    }
});

fastify.route({
    method: 'POST',
    path: '/api/delete',
    onRequest: requiresLogin,
    handler: async (req, res) => {
        try {
            await fsp.rm(path.join(__dirname, 'public', 'uploads', req.user.user), { recursive: true, force: true });
        } catch {}
        users.delete(req.user.user);
        return { success: true };
    }
});

fastify.route({
    method: 'POST',
    path: '/api/register',
    schema: {
        body: {
            type: 'object',
            properties: {
                user: { type: 'string' },
                pass: { type: 'string' }
            },
            required: ["user", "pass"],
            additionalProperties: false
        }
    },
    handler: (req, res) => {
        const { user, pass } = req.body;
        if (user.length < 5 || pass.length < 7) {
            throw new Error("Username or password too short");
        }

        if (!/^[A-Za-z0-9]*$/.test(user)) {
            throw new Error("Username must be alphanumeric");
        }

        if (user.length > 32) {
            throw new Error("Username too long");
        }

        if (users.has(user)) {
            throw new Error("A user already exists with that username");
        }

        users.set(user, {
            user, pass: sha256(pass), pastes: []
        });

        req.session.set("username", user);
        return { success: true };
    }
});

fastify.route({
    method: 'POST',
    path: '/api/login',
    schema: {
        body: {
            type: 'object',
            properties: {
                user: { type: 'string' },
                pass: { type: 'string' }
            }
        },
        required: ["user", "pass"],
        additionalProperties: false
    },
    handler: (req, res) => {
        const { user, pass } = req.body;
        if (user.length < 5 || pass.length < 7) {
            throw new Error("Username or password too short");
        }

        if (!/^[A-Za-z0-9]*$/.test(user)) {
            throw new Error("Username must be alphanumeric");
        }

        if (user.length > 32) {
            throw new Error("Username too long");
        }

        if (!users.has(user)) {
            throw new Error("No user found with that username");
        }

        if (sha256(pass) !== users.get(user).pass) {
            throw new Error("Invalid password");
        }

        req.session.set("username", user);
        return { success: true };
    }
});

let lastVisit = -1;
fastify.route({
    method: 'POST',
    path: '/api/submit',
    schema: {
        body: {
            type: 'object',
            properties: {
                url: { type: 'string' }
            }
        },
        required: ["url"],
        additionalProperties: false
    },
    onRequest: requiresLogin,
    handler: (req, res) => {
        const { url } = req.body;
        if (!url || typeof url !== "string") {
            throw new Error("Missing url");
        }

        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            throw new Error("Invalid url");
        }

        const deltaTime = +new Date() - lastVisit;
        if (deltaTime < 30_000) {
            throw new Error(`Please slow down (wait ${(30_000 - deltaTime)/1000} more seconds)`);
        }
        lastVisit = +new Date();

        bot.visit(url).then(async adminUser => {
            try {
                await fsp.rm(path.join(__dirname, 'public', 'uploads', adminUser), { recursive: true, force: true });
            } catch {}
            users.delete(adminUser);
        });
        return { success: true, message: "An admin will now look over your submission" };
    }
});

const cleanupUploads = async () => {
    const files = await fsp.readdir(path.join(__dirname, 'public', 'uploads'));
    files.filter(f => !f.startsWith(".")).forEach(f => {
        try {
            fsp.rm(path.join(__dirname, 'public', 'uploads', f), { recursive: true, force: true });
        } catch(err) {
            console.log(err);
        }    
    });
};
cleanupUploads();

setInterval(() => {
    console.log("clearing all data...");
    users.clear();
    cleanupUploads();
}, 10 * 60 * 1000);
  
fastify.listen({ port: 3000, host: '0.0.0.0' }, (err, address) => console.log(err ?? `web/burnbin listening on ${address}`));