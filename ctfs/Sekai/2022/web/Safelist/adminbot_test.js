// npm i puppeteer
// script to emulate admin bot

const puppeteer = require("puppeteer");

const FLAG = "SEKAI{testflag}";
const SITE = "http://localhost:1234";

const visit = async (url) => {
    // here's a gift to you:
    // flag format: ^SEKAI{[a-z]+}$
    if (!/^SEKAI{[a-z]+}$/.test(FLAG)) {
        console.log("warning: flag not in correct format");
    }

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
            document.querySelector("input[type=text]").value = flag;
            document.querySelector("input[type=submit]").click();
        }, FLAG);
        await page.waitForNavigation();

        await page.close();
        page = await browser.newPage();

        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
        await page.waitForTimeout(40000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

visit("TARGET_URL");