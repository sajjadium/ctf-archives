const puppeteer = require("puppeteer");

const SITE = process.env.SITE || "http://localhost:8080";

const visit = async (message, jwt) => {
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
        await page.setCookie({
            name: 'auth',
            value: jwt,
            domain: new URL(SITE).host
        });
        await page.setCookie({
            name: 'flag',
            value: process.env.FLAG || "flag{test_flag}",
            domain: new URL(SITE).host
        });

        await page.goto(SITE + "/home", { waitUntil: 'networkidle2' });

        await page.evaluate((message) => {
            document.querySelector("textarea").value = message;
            document.querySelector("#submit-btn").click();  
        }, message);

        await page.waitForTimeout(6000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

module.exports = { visit };