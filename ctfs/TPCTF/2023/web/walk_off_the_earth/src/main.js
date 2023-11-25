const express = require('express');
const session = require('express-session');
const crypto = require('crypto');

const { generatePow, checkPow,sanitize } = require('./utils');
const visit = require('./visit');
const random_bytes = size => crypto.randomBytes(size).toString('hex');
const sha256 = text => crypto.createHash('sha256').update(text).digest('hex');
const app = express();
const difficulty = 7;

app.set('views', './views');
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: false }));
app.use(session({
    cookie: { maxAge: 60*60*1000 },
    secret: random_bytes(64),
    resave: false,
    saveUninitialized: false,
}))


app.use((req, res, next) => {
    if (!req.session.pow) {
        req.session.pow = random_bytes(8);
    }
    next();
});

app.get('/', (req, res) => {
    const desc =`sha256(${req.session.pow} + ???) == ${'0'.repeat(difficulty)}(${difficulty})...`;
    res.render('index', { desc });
});

app.get('/note', (req, res) => {
    res.send(sanitize(req.query.text) || 'No note!');
})

app.post('/visit', async (req, res) => {
    // if (!checkPow(req.session.pow, req.body.pow)) {
    //     res.send('Wrong PoW!');
    //     return;
    // }
    const { path, pow } = req.body;
    if ((pow && typeof pow == 'string') && (sha256(req.session.pow + pow).slice(0, difficulty) == '0'.repeat(difficulty))) {
      req.session.pow = random_bytes(8);
      try {
        const result = await visit(path);
        return res.send(result);
      } catch (e) {
        console.error(e);
        return res.status(500).send('Something wrong');
      }

    } else {
      return res.status(500).send(`Wrong pow...\n sha256(${req.session.pow} + ???) == ${'0'.repeat(difficulty)}(${difficulty})...`);
    }


});

app.use('/static', express.static('./static'));

app.listen(8000);
