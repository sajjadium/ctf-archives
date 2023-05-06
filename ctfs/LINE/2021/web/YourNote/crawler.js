const express = require('express');
const logger = require('morgan');
const createError = require('http-errors');
const puppeteer = require('puppeteer');
const pow = require('proof-of-work')

const app = express();
const host = process.env.APP_HOST || 'localhost:5000';
const base_url = 'http://' + host;
const username = 'admin';
const password = process.env.ADMIN_PASSWORD || 'password';
const pow_complexity = process.env.POW_COMPLEXITY || 1;

app.use(logger('dev'));

const router = express.Router();
router.get('/', async function (req, res, next) {
    const url = req.query.url;
    const proof = req.query.proof;
    const prefix = req.query.prefix;
    if (url && url.startsWith(base_url + '/') &&
        proof && prefix && verify(proof, prefix)) {
        const browser = await puppeteer.launch({
            args: [
                '--no-sandbox',
                '--disable-popup-blocking',
            ],
            headless: true,
        });
        const page = await browser.newPage();

        // login
        await page.goto(base_url + '/login');
        await page.type('input[name=username]', username);
        await page.type('input[name=password]', password);
        await Promise.all([
            page.waitForNavigation({
                waitUntil: 'domcontentloaded',
                timeout: 10000,
            }),
            page.click('button[type=submit]'),
        ]);

        // crawl
        page.goto(url).then(() => {
            res.header('Access-Control-Allow-Origin', '*');
            res.send({msg: 'Thank you for the report!'});
        }).catch((err) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.send({msg: 'ng'});
        });
        setTimeout(() => {
            browser.close()
        }, 60 * 1000)
        return
    }
    res.header('Access-Control-Allow-Origin', '*');
    res.send({msg: 'ng'});
});
app.use(router);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.send('error');
});

module.exports = app;

// proof-of-work verify
const verify = (proof, prefix) => {
    const verifier = new pow.Verifier({
        size: 1024,
        n: 16,
        complexity: pow_complexity,
        prefix: Buffer.from(prefix, 'hex'),
        validity: 60000
    })

    setInterval(() => {
        verifier.reset();
    }, 60000);

    return verifier.check(Buffer.from(proof, 'hex'))
}