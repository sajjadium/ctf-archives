// not the actual admin bot script
// but basically the same :>

// npm install puppeteer
const puppeteer = require("puppeteer");

const path = require("path");
let ext = path.resolve(__dirname, "./extension/");

const TIMEOUT = process.env.TIMEOUT ? parseInt(process.env.TIMEOUT) : 8000;

const visit = async (url) => {
    let browser = await puppeteer.launch({
        headless: false,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            `--disable-extensions-except=${ext}`,
            `--load-extension=${ext}`
        ],
        dumpio: true,
        pipe: true
    });

    let page;
    try {
        page = await browser.newPage();
        await page.goto(url, {
            waitUntil: "networkidle2"
        });
        await page.waitForTimeout(TIMEOUT);
        await page.close();
        page = null;
        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (page) await page.close();
        if (browser) await browser.close();
        resolve();
    }
};

visit("https://styleme.be.ax/styles/i/bb9ac7e1b5d4")