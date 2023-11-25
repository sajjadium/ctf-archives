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
            executablePath: '/usr/bin/chromium-browser',
        });

        page = await browser.newPage();

        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 2000 });

        try {
            let text = new URL(url).searchParams.get('text');
            text = sanitize(text);
            await page.waitForFunction(text => document.write(text), { timeout: 2000 },text);
            res = "ByeBye!";
        } catch (e) {
            if (e instanceof puppeteer.ProtocolError && e.message.includes('Target closed')) {
                return res;
            }
        } finally {
            res = "ByeBye!";
        }
    } catch (e) {
        try { await browser.close(); } catch (e) { }
        return res;
    }
    try { await browser.close(); } catch (e) { }
    return "ByeBye!";
}

module.exports = visit;
