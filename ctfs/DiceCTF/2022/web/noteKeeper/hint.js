const puppeteer = require("puppeteer");

// JWT for user "admin", signed with key "jwt secret"
const JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.rJiXjoimcdCR6d6CwXzB4jY9dHP1YbBraTCRWeYJksU";
const SITE = process.env.SITE || "https://notekeeper.mc.ax";

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

        await page.goto(url);
        await page.waitForTimeout(4000);

        // nice page... oh man i should check my notes!!!

        await page.setCookie({
            name: 'session',
            value: JWT,
            domain: new URL(SITE).host,
            httpOnly: true
        });
        await page.goto(SITE + "/home");
        await page.waitForTimeout(4000);

        // looks good to me!!

        await page.evaluate(() => {
            document.querySelector("#logout") && document.querySelector("#logout").click();
        });
        await page.waitForNavigation();
        await browser.close();
        
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

module.exports = { visit };
