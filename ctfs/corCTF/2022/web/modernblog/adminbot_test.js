// npm i puppeteer
// script to emulate admin bot

const puppeteer = require("puppeteer");

const USERNAME = "YOUR_USER";
const PASSWORD = "TEST_PASSWORD";
const SITE = "https://modernblog.be.ax";

const visit = async (url) => {
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
        await page.goto(SITE + "/login", { timeout: 3000, waitUntil: 'domcontentloaded' });

        await page.type("input[name=user]", USERNAME);
        await page.type("input[name=pass]", PASSWORD);
        await page.click("button[type=submit]");

        await page.waitForTimeout(3000);

        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
        await page.waitForTimeout(5000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

visit("TARGET_URL");