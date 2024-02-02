const puppeteer = require("puppeteer");
const crypto = require("crypto");

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const visit = async (url) => {
    const user = crypto.randomBytes(16).toString("hex");
    const pass = crypto.randomBytes(32).toString("hex");
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: "new",
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
        await page.goto("http://localhost:3000/register", { timeout: 5000, waitUntil: 'domcontentloaded' });

        // create new account
        await page.waitForSelector("button[type=submit]");
        await page.type("input[placeholder='Username']", user);
        await page.type("input[placeholder='Password']", pass);
        await page.click("button[type=submit]");
        await sleep(3000);

        // create paste with flag
        await page.type("input[placeholder='Title']", "Flag");
        await page.type("textarea[placeholder='Paste contents']", "Flag");
        const imgUpload = await page.$("input[type=file]");
        await imgUpload.uploadFile("./flag.png");
        await page.click("button[type=submit]");
        await sleep(3000);

        // go to exploit page
        await page.goto(url, { timeout: 5000, waitUntil: 'domcontentloaded' });
        await sleep(30_000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }

    return user;
};

module.exports = { visit };