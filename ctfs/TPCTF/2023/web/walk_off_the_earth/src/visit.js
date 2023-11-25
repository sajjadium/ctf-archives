const puppeteer = require('puppeteer');
const { sanitize } = require('./utils');

const FLAG = process.env.FLAG || 'flag{test1}';

const BASE_URL = 'http://localhost:8000';

async function visit(path) {
    let browser, page;

    if (!/^\/note\?/.test(path)) {
        return 'Invalid path!';
    }
    const url = new URL(BASE_URL + path);
    let res = FLAG;

    try {
        browser = await puppeteer.launch({
            headless: 'new',
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ],
            executablePath: '/usr/bin/google-chrome-stable',
        });

        page = await browser.newPage();


        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 500 });


        if(!browser.connected){
            return "ByeBye!";
        }

        try {
            let text = new URL(url).searchParams.get('text');
            text = sanitize(text);
            console.log(text);
            await page.waitForFunction(text => document.write(text), { timeout: 500 },text);
            res = "ByeBye!";
        } catch (e) {
            console.log(e);
            if (e instanceof puppeteer.ProtocolError && e.message.includes('Target closed')) {
                return res;
            }
        } finally {
            res = "ByeBye!";
        }
    } catch (e) {
        res = "ByeBye";
        try { await browser.close(); } catch (e) { }
        return res;
    }
    try { await browser.close(); } catch (e) { }
    return "ByeBye!";
}

module.exports = visit;
