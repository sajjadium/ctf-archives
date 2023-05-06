// npm install puppeteer

const puppeteer = require("puppeteer");

// change these
const USERNAME = "ADMIN_ACCOUNT";
const PASSWORD = "ADMIN_PASSWORD";
const SITE = "http://paymentpal.localhost";

const visit = async (url) => {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: 'chrome',
            pipe: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--js-flags=--noexpose_wasm,--jitless",
            ],
            dumpio: true
        });

        let page = await browser.newPage();
        await page.goto(SITE, {
            waitUntil: "networkidle2"
        });

        await page.evaluate((username, password) => {
            document.querySelector("input[name=username]").value = username;
            document.querySelector("input[name=password]").value = password;
            document.querySelector("#login_btn").click();
        }, USERNAME, PASSWORD);
        page.once('dialog', async dialog => {
            await dialog.dismiss();
        });
        await page.waitForNavigation();

        // yeah, this is indeed the payment-pal website :')
        await page.waitForTimeout(1000);

        await page.evaluate(() => {
            document.querySelector("#logout_btn").click();
        });
        await page.waitForTimeout(2000);

        await page.goto(url);
        await page.waitForTimeout(10000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

visit("https://yourwebsite/payload");