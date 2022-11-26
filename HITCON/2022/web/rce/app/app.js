const express = require('express');
const cookieParser = require('cookie-parser')
const crypto = require('crypto');

const randomHex = () => '0123456789abcdef'[~~(Math.random() * 16)];

const app = express();
app.use(cookieParser(crypto.randomBytes(20).toString('hex')));

app.get('/', function (_, res) {
    res.cookie('code', '', { signed: true })
        .sendFile(__dirname + '/index.html');
});

app.get('/random', function (req, res) {
    let result = null;
    if (req.signedCookies.code.length >= 40) {
        const code = Buffer.from(req.signedCookies.code, 'hex').toString();
        try {
            result = eval(code);
        } catch {
            result = '(execution error)';
        }
        res.cookie('code', '', { signed: true })
            .send({ progress: req.signedCookies.code.length, result: `Executing '${code}', result = ${result}` });
    } else {
        res.cookie('code', req.signedCookies.code + randomHex(), { signed: true })
            .send({ progress: req.signedCookies.code.length, result });
    }
});

app.listen(5000);