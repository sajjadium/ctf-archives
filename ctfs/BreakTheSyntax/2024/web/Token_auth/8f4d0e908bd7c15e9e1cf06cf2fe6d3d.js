const express = require("express");
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser')
const app = express();
const db_query = require('./db');
const bcrypt = require('bcryptjs');
const port = 3000;

require("dotenv").config();
app.use(express.json());
app.use(cookieParser());

const mergeInto = (source, target) => {
    for (const k in source) {
        if (typeof source[k] === 'object' && typeof target[k] === 'object') {
            mergeInto(source[k], target[k]);
        } else {
            target[k] = source[k];
        }
    }
}

app.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        req.body = { username, password }; // just in case
        const salt = bcrypt.genSaltSync(10);
        const hash = bcrypt.hashSync(password, salt);

        const users = await db_query('SELECT * FROM users WHERE username=?', [username]);
        if (users.length) {
            return res.status(409).json({ error: 'username in use' });
        }
        db_query('INSERT INTO users (username, password) VALUES (?, ?)', [username, hash]);

        res.sendStatus(201);
    } catch (error) {
        res.status(500).json({ error: 'Registration failed' });
    }
})

app.post("/login", async (req, res) => {
    try {
        const { username, password } = req.body;
        req.body = { username, password }; // just in case

        const user = (await db_query('SELECT * FROM users WHERE username = ?', [username]))[0];

        if (!user) {
            return res.status(401).json({ error: 'Authentication failed' });
        }
        const passwordMatch = bcrypt.compareSync(password, user.password);

        if (!passwordMatch) {
            return res.status(401).json({ error: 'Authentication failed' });
        }

        restricted = { username: {}, password: {} }
        // make sure new account is not admin
        restricted.admin = undefined;
        mergeInto(req.body, restricted);

        try {
            const token = jwt.sign(restricted, process.env.JWT_SECRET, {
                expiresIn: '1h',
            });
            res.cookie('access_token', token, {
                httpOnly: true,
                secure: true
            });
            res.sendStatus(200);
        } catch (error) {
            res.status(500).json({ error: 'JWT error.' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Login failed' });
    }
});

app.get('/flag', (req, res) => {
    const token = req.cookies.access_token;
    let data = {};
    if (token)
        data = jwt.verify(token, process.env.JWT_SECRET);

    // hopefully, it's impossible to be an admin yet
    if (data.admin)
        res.status(200).send(process.env.FLAG);
    else
        res.sendStatus(403);
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
