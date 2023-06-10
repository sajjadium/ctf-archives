const serialize = require('serialize-javascript');
const xssFilters = require('xss-filters')

const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const fileupload = require("express-fileupload");
const cookieParser = require('cookie-parser');

const fs = require('fs');
const crypto = require('crypto');

const app = express();

app.use(cookieParser());

app.use((req, res, next) => {
    res.set("Content-Security-Policy", "default-src 'self' www.youtube.com");
    next();
})

app.use(session({
    secret: crypto.randomBytes(32).toString('hex'),
    saveUninitialized: true,
}));

app.use(fileupload());
app.use(bodyParser.urlencoded({ extended: false }))

app.use('/static', express.static('static'));
app.use('/uploads', express.static('uploads'));

app.all('/', (req, res) => {

    const nonce = crypto.randomBytes(32).toString('hex');

    res.set("Content-Security-Policy", "default-src 'self' www.youtube.com 'nonce-" + nonce + "'");

    let scriptElement = `<script nonce="${nonce}">`;

    if (req.session.username && req.session.cereal) {
        scriptElement += "window.__SESSION__ ="
        try {
            scriptElement += serialize({
                username: xssFilters.inDoubleQuotedAttr(req.session.username),
                cereal: new URL(xssFilters.inDoubleQuotedAttr(req.session.cereal))
            })
        }
        catch (e) {
            req.session.username = null;
            req.session.cereal = null;
            scriptElement += serialize({})
        }
    }

    scriptElement += "</script>";

    const html = fs.readFileSync('index.html', 'utf8').replace('<!-- SCRIPT -->', scriptElement);
    res.send(html);
});

app.all('/set', (req, res) => {
    req.session.username = req.param('username');
    req.session.cereal = req.param('cereal');
    res.redirect('/');
});

app.all('/upload', (req, res) => {
    const file = req.files.cereal;
    const hash = crypto.createHash('sha256');
    hash.update(file.data);
    const filename = hash.digest('hex');

    fs.writeFileSync(`uploads/${filename}.png`, file.data);
    res.json({ url: `http://${req.headers.host}/uploads/${filename}.png` });
})

app.all('/flag', (req, res) => {
    if (req.cookies && req.cookies.secret === process.env.SECRET) {
        res.send(process.env.FLAG);
    } else {
        res.send('Nope');
    }
})

app.listen(80, () => {
    console.log('Server listening on port 80');
})