const app = require('fastify')();
const fs = require('fs');
const sqlite3 = require('sqlite3');
const bcrypt = require('bcrypt');
const path = require('path');
const crypto = require('crypto');

const db = new sqlite3.Database('database.db');

db.run('CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, username TEXT UNIQUE, pfpPath TEXT, password TEXT);', err => {
    const adminPassword = fs.readFileSync(path.join(__dirname, 'admin-password.txt')).toString().trim();
    const id = generateId();
    db.run('INSERT OR IGNORE INTO users (id, username, password, pfpPath) VALUES (?, ?, ?, ?)', [id, 'admin', bcrypt.hashSync(adminPassword, 10), 'default.png']);
    db.run('CREATE TABLE IF NOT EXISTS jokes (id TEXT PRIMARY KEY, author TEXT, prompt TEXT, punchline TEXT);', err => {
        const flag = fs.readFileSync(path.join(__dirname, 'flag.txt')).toString();
        db.run('INSERT INTO jokes (id, author, prompt, punchline) VALUES (?, ?, ?, ?)', [generateId(), id, 'I used to be addicted to quoting Taylor Swift...', flag]);
    });
});


app.register(require('fastify-formbody'));

app.register(require('middie'))
    .register(require('fastify-file-upload'), {
        limits: { fileSize: 1024 * 1024 }
    });

app.register(require('fastify-cookie'))
    .register(require('@fastify/session'), {
        secret: crypto.randomBytes(20).toString('hex'),
        cookie: { secure: false }
    });

app.register(require('fastify-helmet'), {
    contentSecurityPolicy: {
        directives: {
            scriptSrc: ["'none'"],
            imgSrc: ["*", "data:"],
            styleSrc: ["'self'", "fonts.googleapis.com"]
        }
    }
});

app.register(require('fastify-static'), {
    root: path.join(__dirname, 'static'),
    prefix: '/static/',
    decorateReply: false
});

app.register(require('fastify-static'), {
    root: path.join(__dirname, 'uploads'),
    prefix: '/uploads/',
    decorateReply: false
});

app.register(require('point-of-view'), {
    engine: {
        ejs: require('ejs')
    }
});

app.addHook('preHandler', (req, res, next) => {
    res.locals = {
        session: req.session,
    };
    next();
});

app.get('/', (req, res) => {
    res.view('/templates/index.ejs', { 'title': '' });
});


app.get('/login', (req, res) => {
    if (req.session.user)
        return res.redirect('/');

    res.view('/templates/login.ejs', { 'title': 'Login' });
});


app.post('/login', (req, res) => {
    db.get('SELECT * FROM users WHERE username = ?;', [req.body.username], (err, user) => {
        if (err || !user)
            return res.view('/templates/login.ejs', { 'title': 'Login', 'error': 'Invalid username or password' });

        if (bcrypt.compareSync(req.body.password, user.password)) {
            req.session.user = user;

            res.redirect('/');
        } else {
            res.view('/templates/login.ejs', { 'title': 'Login', 'error': 'Invalid username or password' });
        }
    });
});


app.get('/register', (req, res) => {
    res.view('/templates/register.ejs', { 'title': 'Register' });
});

function generateId() {
    const ALLOWED = 'abcdefghijklmnopqrstuvwxyz0123456789-_';
    let id = '';
    for (let i = 0; i < 8; i++) {
        id += ALLOWED[Math.floor(Math.random() * ALLOWED.length)];
    }

    return id;
}

app.post('/register', (req, res) => {
    const { username, password, confirm } = req.body;

    if (password !== confirm)
        return res.view('/templates/register.ejs', { 'title': 'Register', 'error': 'Passwords do not match' });

    const id = generateId();

    const passwordHash = bcrypt.hashSync(password, 10);

    db.run('INSERT INTO users (id, username, password, pfpPath) VALUES (?, ?, ?, ?);', [id, username, passwordHash, 'default.png'], err => {
        if (err)
            return res.view('/templates/register.ejs', { 'title': 'Register', 'error': 'Username already taken' });

        req.session.user = {
            id: id,
            username: username,
            password: passwordHash,
            pfpPath: 'default.png'
        };

        res.redirect('/');
    });
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});


app.get('/make', (req, res) => {
    if (!req.session.user)
        return res.redirect('/login');

    res.view('/templates/make.ejs', { 'title': 'Make' });
});

app.post('/make', (req, res) => {
    if (!req.session.user)
        return res.redirect('/login');

    const { prompt, punchline } = req.body;

    const id = generateId();

    db.run('INSERT INTO jokes (id, author, prompt, punchline) VALUES (?, ?, ?, ?);', [id, req.session.user.id, prompt, punchline], err => {
        if (err)
            return res.status(500).send('Internal Server Error');

        res.redirect(`/joke/${id}`);
    });
});

app.get('/profile/edit', (req, res) => {
    res.view('/templates/profile-edit.ejs', { 'title': 'Edit Profile' });
});

app.post('/profile/edit', (req, res) => {
    if (!req.session.user)
        return res.status(401).send('Unauthorized');

    const { username, password, confirm } = req.body;

    if (!bcrypt.compareSync(confirm, req.session.user.password))
        return res.view('/templates/profile-edit.ejs', { 'title': 'Edit Profile', 'error': 'Confirm password is incorrect' });

    let pfp, pfpPath;
    if (req.raw.files && req.raw.files.pfp && req.raw.files.pfp.size > 0) {
        pfp = req.raw.files.pfp;
        pfpPath = req.session.user.id + path.extname(pfp.name);
    }

    const newUsername = username || req.session.user.username;
    const newHash = password ? bcrypt.hashSync(password, 10) : req.session.user.password;
    const newPfpPath = pfpPath || req.session.user.pfpPath;

    db.run('UPDATE users SET username = ?, password = ?, pfpPath = ? WHERE id = ?;', [newUsername, newHash, newPfpPath, req.session.user.id], err => {
        if (err)
            return res.status(500).send('Internal Server Error');

        if (pfp && pfp.size > 0) {
            const p = path.join(__dirname, 'uploads', newPfpPath);
            fs.writeFileSync(p, pfp.data);
        }

        req.session.user = {
            id: req.session.user.id,
            username: newUsername,
            password: newHash,
            pfpPath: newPfpPath
        }

        return res.redirect('/');
    });
});

app.get('/profile/:id', (req, res) => {
    db.get('SELECT * FROM users WHERE id = ?;', [req.params.id], (err, user) => {
        if (err || !user) {
            return res.status(404).send('Not Found');
        }

        db.all('SELECT * FROM jokes WHERE jokes.author = ?;', [req.params.id], (err, rows) => {
            if (err) {
                return res.status(500).send('Internal Server Error');
            }

            res.view('/templates/profile.ejs', { 'title': 'Profile', 'user': user, 'jokes': rows });
        });
    });
});

app.get('/joke/:id', (req, res) => {
    db.get('SELECT jokes.id, jokes.author, jokes.prompt, jokes.punchline, users.username, users.pfpPath FROM jokes INNER JOIN users ON jokes.author = users.id WHERE jokes.id = ?;', [req.params.id], (err, joke) => {
        if (err || !joke) {
            return res.status(404).send('Not Found');
        }

        return res.view('/templates/joke.ejs', { 'title': joke.prompt, 'joke': joke });
    });
});

app.listen(3000, '0.0.0.0', (err, address) => {
    if (err) {
        app.log.error(err);
        process.exit(1);
    }

    console.log(`Server listening on ${address}`);
});
