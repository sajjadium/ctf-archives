const app = require('fastify')({ logger: true });
const crypto = require('crypto');
const { v4 } = require('uuid');
const jwt = require('jsonwebtoken');

const secret = crypto.randomBytes(32).toString('hex');

const db = {};

app.register(require('@fastify/cookie'));

app.register(require('@fastify/view'), {
    engine: {
        ejs: require('ejs')
    }
});

app.register(require('@fastify/formbody'));

app.decorateRequest('locals', null);
app.addHook('onRequest', (req, res, next) => {
    if (!req.cookies.token) {
        req.locals = {};
        return next();
    }

    try {
        req.locals = jwt.verify(req.cookies.token, secret);
    } catch (err) {
        req.locals = {};
    }

    req.locals.nonce = req.locals.nonce ?? '47baeefe8a0b0e8276c2f7ea2f24c1cc9deb613a8b9c866f796a892ef9f8e65d';
    req.locals.nonce = crypto.createHash('sha256').update(req.locals.nonce).digest('hex');
    res.header('Content-Security-Policy', `script-src 'nonce-${req.locals.nonce}'; default-src 'self'; style-src 'self' 'nonce-${req.locals.nonce}';`);

    req.locals.userId ??= v4();

    next();
});

app.addHook('preHandler', (req, res, next) => {
    res.cookie('token', jwt.sign(req.locals, secret), {
        path: '/',
    });

    next();
});


app.get('/', (req, res) => {
    return res.view('views/index.ejs', {
        nonce: req.locals.nonce,
    });
}).post('/', (req, res) => {
    const { name, toDo } = req.body;

    if (req.locals.userId === undefined)
        return res.status(400).send('Bad request');

    db[req.locals.userId] = { name, toDo };

    return res.redirect('/do/' + req.locals.userId);
});

app.get('/do/:id', (req, res) => {
    const item = db[req.params.id];

    if (!item) {
        return res.status(404).send('Not found');
    }

    return res.view('views/do.ejs', {
        nonce: req.locals.nonce,
        isSelf: req.locals.userId === req.params.id,
        ...item
    });
});

app.get('/do', (req, res) => {
    return res.redirect('/do/' + req.locals.userId);
});

app.listen({
    port: 3000,
    host: '0.0.0.0',
    listeningListener: (address) => {
        app.log.info(`server listening on ${address}`);
    }
});
