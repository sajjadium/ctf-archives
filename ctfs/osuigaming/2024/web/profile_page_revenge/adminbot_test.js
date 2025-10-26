// admin bot test script
// npm i puppeteer
const puppeteer = require("puppeteer");

const FLAG = "osu{test_flag}";
const SITE = "https://profile-page-revenge.web.osugaming.lol";

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function visit(url) {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true,
            pipe: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--js-flags=--noexpose_wasm,--jitless",
            ],
            dumpio: true
        });

        let page = await browser.newPage();
        await page.goto(SITE, { timeout: 3000, waitUntil: 'domcontentloaded' });

        await page.evaluate((flag) => {
            document.cookie = "flag=" + flag + "; secure; path=/";
        }, FLAG);

        await page.close();
        page = await browser.newPage();

        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
        await sleep(5000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
}

visit("EXPLOIT_URL");