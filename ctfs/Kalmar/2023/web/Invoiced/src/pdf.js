const puppeteer = require('puppeteer');
const querystring = require("querystring");

const browser_options = {
    args: [
        '--disable-background-networking',
        '--disable-default-apps',
        '--no-sandbox',
        '--disable-extensions',
        '--disable-gpu',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update'
    ],
    pipe: true,
    headless: true
};

const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

async function renderPdf(body){
    const browser = await puppeteer.launch(browser_options);
    const page = await browser.newPage();
    const cookie = {
        "name": "bot",
        "value": "true",
        "domain": "localhost:5000",
        "httpOnly": true,
        "sameSite": "Strict"
    }
    await page.setCookie(cookie)
    await page.goto("http://localhost:5000/renderInvoice?"+querystring.stringify(body), { waitUntil: 'networkidle0' });
    await delay(1000)
    const pdf = await page.pdf({ format: 'A4' });
    await browser.close();
    return pdf
}

module.exports = { renderPdf };