// npm i puppeteer
// script to emulate admin bot
const puppeteer = require("puppeteer");

const FLAG = "dice{test_flag}";
const SITE = "https://calculator-2.mc.ax";

const sleep = ms => new Promise(r => setTimeout(r, ms));

const visit = async (url) => {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: 'new',
            pipe: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--js-flags=--noexpose_wasm,--jitless",
            ],
            dumpio: true
        });

        const context = await browser.createIncognitoBrowserContext();
        const page = await context.newPage();

        await page.setCookie({
            name: 'flag',
            value: FLAG,
            domain: new URL(SITE).host
        });
        await page.goto(url, { timeout: 5000, waitUntil: 'domcontentloaded' });
        await sleep(5000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

visit("EXPLOIT_PAGE");
