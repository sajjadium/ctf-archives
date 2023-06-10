const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const path = require('path');

const app = express();

app.use(express.static('static'))

app.use(session({
    secret: crypto.randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: false,
    cookie: { sameSite: 'lax' }
}))

app.use(bodyParser.urlencoded({ extended: false }));

const initSession = (req, res, next) => {
    if (!req.session.notes) {
        req.session.notes = [];
    }
    next();
}

app.get('/', initSession, (req, res) => {
    const query = req.query.q;

    if (!query) {
        return res.sendFile(path.join(__dirname, 'index.html'));
    }

    const found = req.session.notes.filter(note => note.text.includes(query));

    if (!found.length) {
        return res.redirect('/?found=0');
    }
    return res.redirect(`/?found=1#${btoa(JSON.stringify(found.map(note => note.id)))}`);
})

app.post('/save', initSession, (req, res) => {
    req.session.notes.push({ id: req.session.notes.length, text: req.body.note });
    return res.redirect('/');
})

app.get('/notes', initSession, (req, res) => {
    return res.json(req.session.notes);
})

app.listen(80, () => console.log('Listening on port 80'));