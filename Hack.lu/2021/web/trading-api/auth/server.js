const express = require('express');
const dotenv = require('dotenv');
const morgan = require('morgan');

const getOrDefault = (key, defaultValue) => {
    if (!process.env.hasOwnProperty(key)) {
        return defaultValue;
    }

    return process.env[key];
}
const getRequired = (key) => {
    if (!process.env.hasOwnProperty(key)) {
        console.error(`Missing config: ${key}`);
        process.exit(1);
    }

    return process.env[key];
};

dotenv.config();
const HOST = getOrDefault('HOST', '127.0.0.1');
const PORT = getOrDefault('PORT', '3001');
const TOKEN = getRequired('TOKEN');
const CREDENTIALS = JSON.parse(getOrDefault('CREDENTIALS', '[]'));

const app = express();
app.use(morgan('dev'));
app.use(express.json());

const ensureValidToken = (req, res, next) => {
    const token = req.get('authorization') ?? null;
    if (token === null) {
        return res.status(400).end();
    }
    if (token !== TOKEN) {
        return res.status(401).end();
    }
    next();
};

const checkCredentials = (username, password) => {
    console.log(`Checking ${JSON.stringify(username)}:${JSON.stringify(password)}`);
    return CREDENTIALS.some(({ user, pass }) => username === user && password === pass);
};

app.all('/health', (req, res) => res.send('ok'));

app.post('/api/users/:username/auth', ensureValidToken, async (req, res) => {
    const { username } = req.params;
    const { password } = req.body;

    try {
        if (checkCredentials(username, password)) {
            return res.status(200).end();
        } else {
            return res.status(401).end();
        }
    } catch (error) {
        console.error(error);
        return res.status(500).end();
    }
});

app.listen(PORT, HOST, () => {
    console.log(`Listening on ${HOST}:${PORT}`);
});
