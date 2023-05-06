const dotenv = require('dotenv');
const express = require('express');
const morgan = require('morgan');
const session = require('express-session');
const connectRedis = require('connect-redis');
const hbs  = require('express-handlebars');

dotenv.config();
const { redisClient, db } = require('./db');

const die = (msg) => {
    console.log(msg);
    process.exit(1);
};

const HOST = process.env.HOST ?? '127.0.0.1';
const PORT = process.env.PORT ?? '3000';
const SESSION_SECRET = process.env.SESSION_SECRET ?? die('missing SESSION_SECRET');

const app = express();
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: false }));

// views
app.engine('handlebars', hbs());
app.set('view engine', 'handlebars');

// session
const RedisStore = connectRedis(session);
app.use(session({
    store: new RedisStore({ client: redisClient }),
    secret: SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false,
        httpOnly: true,
    },
}));

// flash
app.use((req, res, next) => {
    const { render } = res;
    req.session.flash = req.session.flash ?? [];
    res.render = (template, options={}) => {
        render.call(res, template, {
            user: req.session?.user,
            flash: req.session.flash,
            ...options,
        });
        req.session.flash = [];
    };
    res.flash = (level, message) => {
        req.session.flash.push({ level, message });
    };
    next();
});

app.get('/', (req, res) => res.render('index'));

app.get('/register', (req, res) => res.render('register'));
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password
        || typeof username !== 'string' || typeof password !== 'string'
        || /[^\w]/i.test(username)) {
        res.flash('danger', 'invalid username or password');
        return res.status(400).render('register');
    }

    try {
        await db.createUser(username, password);
        res.redirect('/login');
    } catch (error) {
        console.error('create user error:', error?.message)
        res.flash('danger', `Error: ${error?.message}`);
        res.render('register');
    }
});

app.get('/login', (req, res) => res.render('login'));
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
        res.flash('danger', 'invalid username or password');
        return res.status(400).render('login');
    }

    const user = await db.getUserByNameAndPassword(username, password);
    if (!user) {
        res.flash('danger', 'invalid username or password');
        return res.status(401).render('login');
    }

    await db.addSessionToUser(user.id, req.sessionID);
    req.session.user = user;
    res.redirect('/notes');
});

const ensureAuth = (req, res, next) => {
    if (!req.session?.user?.id) {
        res.flash('warning', 'Login required');
        return res.redirect('/login');
    }
    next();
};

app.post('/logout', ensureAuth, (req, res) => {
    const sid = req.sessionID;
    const uid = req.session.user.id;
    req.session.destroy(async (error) => {
        if (error) {
            console.error('logout error:', error?.message);
        }
        await db.removeSessionFromUser(uid, sid);
        res.clearCookie('connect.sid');
        res.redirect('/login');
    });
});

app.get('/notes', ensureAuth, async (req, res) => {
    const notes = await db.getUserNotes(req.session.user.id);
    res.render('notes', { notes });
});
app.get('/notes/:nid', ensureAuth, async (req, res) => {
    const { nid } = req.params;
    if (!await db.hasUserNoteAcess(req.session.user.id, nid)) {
        return res.redirect('/notes');
    }
    const note = await db.getNote(nid);
    res.render('note', { note });
});
app.post('/notes', ensureAuth, async (req, res) => {
    let { title, content } = req.body;
    if (req.query.random) {
        const ms = Math.floor(2000 + Math.random() * 1000);
        await new Promise(r => setTimeout(r, ms));
        res.flash('info', `Our AI ran ${ms}ms to generate this piece of groundbreaking research.`);
        content = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.';
    }

    if (!title || !content || typeof title !== 'string' || typeof content !== 'string') {
        res.flash('danger', 'invalid title or content');
        return res.status(400).render('notes');
    }

    const nid = await db.createNote(title, content);
    await db.addNoteToUser(req.session.user.id, nid);

    res.flash('success', `Note ${nid} was created!`);
    res.redirect('/notes');
}); 

app.get('/me', ensureAuth, (req, res) => res.render('me', { user: req.session.user }));
app.post('/deleteme', ensureAuth, async (req, res) => {
    await db.deleteUser(req.session.user.id);
    req.session.destroy(async (error) => {
        if (error) {
            console.error('deleteme error:', error?.message);
        }
        res.clearCookie('connect.sid');
        res.redirect('/login');
    });
});

app.listen(PORT, HOST, () => console.log(`Listening on ${HOST}:${PORT}`));
