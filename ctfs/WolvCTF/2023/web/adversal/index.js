const express = require('express');
const puppeteer = require('puppeteer');
const sessions = require('client-sessions');
const randomstring = require("randomstring");
const escape = require('escape-html');
const path = require('path');

const app = express()

const FLAG = process.env.FLAG || 'wctf{redacted}'
const SECRET = process.env.SECRET || 'redacted'
const CHAL_URL = 'http://0:8080'

app.use(express.static(__dirname + '/public'))
app.use(sessions({
    cookieName: 'session',
    secret: SECRET,
    duration: 24 * 60 * 60 * 1000,
    activeDuration: 1000 * 60 * 5
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// This is the endpoint the admin bot will visit (with your supplied ad as the 'ad' query parameter)
app.get('/otp', (req, res) => {
    let defaultAd = `
        <img src="imgs/logo.png" /> <br/>
        <link rel="stylesheet" href="style/style.css" />
        <h3>Get your <a href="https://wolvsec.org/" target="_blank">WolvSec</a> merch!</h3>
    `
    let ad = req.query.ad || defaultAd; 

    // Imagine that the OTP gets used somewhere important
    //  (you will need to exfiltrate it from the admin bot to get the flag)
    let otp = randomstring.generate({length: 12, charset: 'alphanumeric'});

    res.set("Content-Security-Policy", "script-src 'none'; object-src 'none'; connect-src 'self';");

    res.render('otp', {
        otp: otp,
        ad: ad
    });
});

const visitUrl = async (url, cookieDomain) => {
    // Chrome generates this error inside our docker container when starting up.
    // However, it seems to run ok anyway.
    //
    // [0105/011035.292928:ERROR:gpu_init.cc(523)] Passthrough is not supported, GL is disabled, ANGLE is

    let browser =
            await puppeteer.launch({
                headless: true,
                pipe: true,
                dumpio: true,
                ignoreHTTPSErrors: true,

                // headless chrome in docker is not a picnic
                args: [
                    '--incognito',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                ]
            })

    try {
        const ctx = await browser.createIncognitoBrowserContext()
        const page = await ctx.newPage()

        let otp = null;
        try {
            await page.setUserAgent('puppeteer');
            await page.goto(url, { timeout: 20000, waitUntil: 'networkidle2' })
            otp = await page.$eval("input", element=> element.getAttribute("value"));
        } finally {
            await page.close()
            await ctx.close()
        }
        return otp;
    }
    finally {
        browser.close()
    }
}

app.get('/visit', async (req, res) => {
    const ad = req.query.ad
    console.log('received ad: ', ad)

    let url = CHAL_URL + '/otp?ad=' + ad;

    try {
        console.log('visiting url: ', url)
        let otp = await visitUrl(url, req.hostname)
        if(otp != null) {
            req.session.otp = otp;
            res.redirect('done.html');
        } else {
            res.send('Error: evaluator could not find the OTP element on the page')
        }
    } catch (e) {
        console.log('error visiting: ', url, ', ', e.message)
        res.send('Error visiting page with your ad: ' + escape(e.message))
    } finally {
        console.log('done visiting url: ', url)
    }
});

app.get('/flag', (req, res) => {
    if(req.query.otp && req.session.otp && req.query.otp === req.session.otp) {
        res.send(FLAG);
    } else {
        res.send('Incorrect! <a href="/index.html">Back to home</a>');
    }
});

const port = 8080
app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})