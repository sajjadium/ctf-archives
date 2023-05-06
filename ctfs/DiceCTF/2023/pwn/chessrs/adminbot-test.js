// npm i puppeteer
// script to emulate admin bot

const puppeteer = require("puppeteer");

const FLAG = "flag{test_flag}";

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    })
}

const visit = async (url) => {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true,
            pipe: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
            dumpio: true
        });
        
        const page = await browser.newPage();
        await page.goto('https://chessrs.mc.ax', { timeout: 3000, waitUntil: 'domcontentloaded' });
        await page.evaluate(flag => {
            document.cookie = `flag=${flag}`;
        }, FLAG);
        await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
        await sleep(3000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

// place your exploit URL here
visit("EXPLOIT_URL");