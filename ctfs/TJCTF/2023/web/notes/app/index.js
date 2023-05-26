const express = require('express');
const app = express();
const session = require('express-session');
const fs = require('fs');
const mysql = require('mysql2');
const { v4 } = require('uuid');

const pool = mysql.createPool({
    host: process.env.MYSQL_HOST || 'localhost',
    database: 'db',
    port: 3306,
    user: 'root',
    password: 'lmao',
    connectionLimit: 10
});

const flag = fs.readFileSync('flag.txt', 'utf8').trim();

app.use(session({
    secret: require('crypto').randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true
}));

const sessions = {};
function associateSessionWithUser(user_id, session) {
    session.user_id = user_id;
    if (user_id in sessions)
        sessions[user_id].push(session);
    else
        sessions[user_id] = [session];
}

app.use(express.urlencoded({ extended: false }));

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    if (!req.session.user_id) {
        return res.redirect('/login?e=login%20to%20make%20notes');
    }

    pool.query(`SELECT * FROM notes WHERE user_id = '${req.session.user_id}';`, (err, results) => {
        pool.query(`SELECT * FROM users WHERE id = '${req.session.user_id}';`, (err, users) => {
            res.render('index', { notes: results, user: users[0] || { username: flag } });
        });
    });
});

app.get('/login', (req, res) => {
    if (req.session.user_id)
        return res.redirect('/');

    res.render('login');
});

app.post('/login', (req, res) => {
    if (req.session.user_id)
        return res.redirect('/');

    if (!req.body.username || !req.body.password)
        return res.redirect('/login?e=missing%20fields');

    pool.query(`SELECT * FROM users WHERE username = '${req.body.username}';`, (err, results) => {
        if (err) {
            res.redirect('/login?e=an%20error%20occurred');
        } else {
            if (results.length === 0) {
                res.redirect('/login?e=user%20not%20found');
            } else {
                if (results[0].password === req.body.password) {
                    associateSessionWithUser(results[0].id, req.session);
                    res.redirect('/');
                } else {
                    res.redirect('/login?e=incorrect%20password');
                }
            }
        }
    });
});

app.get('/register', (req, res) => {
    if (req.session.user_id)
        return res.redirect('/');

    res.render('register');
});

app.post('/register', (req, res) => {
    if (req.session.user_id)
        return res.redirect('/');

    if (!req.body.username || !req.body.password)
        return res.redirect('/register?e=missing%20fields');

    const id = v4();
    pool.query(`INSERT INTO users (id, username, password) VALUES ('${id}', '${req.body.username}', '${req.body.password}');`, (err, results) => {
        if (err) {
            res.redirect('/register?e=user%20already%20exists');
        } else {
            associateSessionWithUser(id, req.session);
            res.redirect('/');
        }
    });
});

app.post('/user/delete', (req, res) => {
    const id = req.session.user_id;

    pool.query(`DELETE FROM users WHERE id = '${id}' AND password = '${req.body.password}';`, (err, results) => {

        pool.query(`SELECT * FROM users WHERE id = '${id}' AND password != '${req.body.password}';`, (err, results) => {

            if (err)
                return res.redirect('/?e=an%20error%20occurred');

            if (results.length !== 0)
                return res.redirect('/?e=incorrect%20password');

            sessions[id].forEach(session => {
                session.destroy();
            });

            pool.query(`DELETE FROM notes WHERE user_id = '${id}';`, (err, results) => {
                if (err) {
                    res.json({ success: false, message: err });
                } else {
                    res.redirect('/');
                }
            });
        });
    });
});

app.post('/note/create', (req, res) => {
    pool.query(`INSERT INTO notes (note, user_id) VALUES ('${req.body.note}', '${req.session.user_id}');`, (err, results) => {
        if (err) {
            res.send(err);
        } else {
            res.redirect('/');
        }
    });
});

// Just to make sure the server is properly started
app.get('/probe', (req, res) => {
    pool.query(`SELECT * FROM notes;`, (err, results) => {
        if (err) {
            res.status(500).send('Internal Server Error');
        } else {
            res.status(200).send('OK');
        }
    });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
