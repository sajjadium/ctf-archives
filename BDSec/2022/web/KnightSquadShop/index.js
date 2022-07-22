const express = require('express')
const session = require('express-session')
const fs = require('fs')

const app = express()

const products = require('./product.json')


const product = {
    name: 'Some Product',
    price: 100,
    description: 'A description of the product',
    quantity: 1,
};

products['flags'] = {
    name: 'Get flags',
    price: 2.5e+25,
    description: fs.readFileSync('flag.txt', 'utf8').trim(),
    quantity: 1
}

app.use(express.json({ extended: true }));
app.set('view engine', 'ejs');

app.use(session({
    secret: require('crypto').randomBytes(64).toString('hex'),
    resave: false,
    saveUninitialized: true,
}));

app.use((req, res, next) => {
    if(req.session.money !== undefined) {
        return next();
    }
    req.session.money = 100;

    if (req.ip == '127.0.0.1') {
        req.session.admin = true;
    }
    next();
});

app.get('/', (req, res) => {
    res.render('index', { products, money: req.session.money})
})

app.post('/api/v1/sell', (req, res) => {
    for (const [key, value] of Object.entries(req.body)) {
        if (key === 'flags' && !req.session.admin) {
            continue;
        }

        if (!products[key]) {
            products[key] = JSON.parse(JSON.stringify(product));
        }

        for (const [k, v] of Object.entries(value)) {
            if (k === 'quantity') {
                products[key][k] += v;
            } else {
                products[key][k] = v;
            }
        }
    }

    res.send('Sell successful');
});

app.post('/api/v1/buy', (req, res) => {
    const { product, quantity } = req.body;

    if (typeof product === 'undefined' || typeof quantity !== 'number' || quantity <= 0 || !products[product]) {
        return res.status(400).send('Invalid request');
    }

    if (products[product].quantity >= quantity) {
        if (req.session.money >= products[product].price * quantity) {
            products[product].quantity -= quantity;
            req.session.money -= products[product].price * quantity;
            res.json(products[product]);
        } else {
            res.status(402).send('Not enough money');
        }
    } else {
        res.status(451).send('Not enough product');
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
