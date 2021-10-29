const got = require('got');
const jsonwebtoken = require('jsonwebtoken');
const uuid = require('uuid').v4;
const { getRequired, getOrDefault, getOrGenerate } = require('./config');

const AUTH_SERVICE = getOrDefault('AUTH_SERVICE', 'http://localhost:3001');
const AUTH_API_TOKEN = getRequired('AUTH_API_TOKEN');
const JWT_SECRET = getOrGenerate('JWT_SECRET', uuid);

async function login(req, res) {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).send('missing username or password');
    }

    try {
        const r = await got.post(`${AUTH_SERVICE}/api/users/${encodeURI(username)}/auth`, {
            headers: { authorization: AUTH_API_TOKEN },
            json: { password },
        });
        if (r.statusCode !== 200) {
            return res.status(401).send('wrong');
        }

        const jwt = jsonwebtoken.sign({ username }, JWT_SECRET);
        return res.json({ token: jwt });
    } catch (error) {
        return res.status(503).end('error');
    }
}

function authn(req, res, next) {
    const authHeader = req.header('authorization');
    if (!authHeader) {
        return res.status(400).send('missing auth token');
    }
    try {
        req.user = jsonwebtoken.verify(authHeader, JWT_SECRET);
        next();
    } catch (error) {
        return res.status(401).send('invalid auth token');
    }
}

module.exports = {
    login,
    authn,
};
