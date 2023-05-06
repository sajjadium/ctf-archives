const express = require('express');
const session = require('express-session');
const fs = require('fs');

const app = express();

const fruits = require('./inventory.json');

const fruit = {
    name: 'some fruit',
    price: 0.25,
    description: 'a fruit',
    quantity: 1
};

fruits['grass'] = {
    name: 'grass',
    price: 2.5e+25,
    description: fs.readFileSync('flag.txt', 'utf8').trim(),
    quantity: 1
};

app.use(express.json({ extended: true }));

app.set('view engine', 'ejs');

app.use(session({
    secret: require('crypto').randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

app.use((req, res, next) => {
    if (req.session.money !== undefined)
        return next();

    req.session.money = 5;

    if (req.ip == '127.0.0.1') {
        req.session.admin = true;
    }

    next();
});

app.get('/', (req, res) => {
    res.render('index', { fruits, money: req.session.money });
});

app.post('/api/v1/sell', (req, res) => {
    for (const [key, value] of Object.entries(req.body)) {
        if (key === 'grass' && !req.session.admin) {
            continue;
        }

        if (!fruits[key]) {
            fruits[key] = JSON.parse(JSON.stringify(fruit));
        }

        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                fruits[key][k] += v;
            } else {
                fruits[key][k] = v;
            }
        }
    }

    res.send('Sell successful');
});

app.post('/api/v1/buy', (req, res) => {
    const { fruit, quantity } = req.body;

    if (typeof fruit === 'undefined' || typeof quantity !== 'number' || quantity <= 0 || !fruits[fruit]) {
        return res.status(400).send('Invalid request');
    }

    if (fruits[fruit].quantity >= quantity) {
        if (req.session.money >= fruits[fruit].price * quantity) {
            fruits[fruit].quantity -= quantity;
            req.session.money -= fruits[fruit].price * quantity;
            res.json(fruits[fruit]);
        } else {
            res.status(402).send('Not enough money');
        }
    } else {
        res.status(451).send('Not enough fruit');
    }
});

app.post('/api/v1/money', (req, res) => {
    if (req.session.admin) {
        req.session.money += req.body.money;
        res.send('Money added');
    } else {
        res.status(403).send('Not admin');
    }
});

app.listen(3000, () => {
    console.log('Listening on port 3000');
});
