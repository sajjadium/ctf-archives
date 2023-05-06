const puppeteer = require("puppeteer");
const path = require("path");

let ext = path.resolve(__dirname, "./extension/");

let queue = [];
const addToQueue = (url) => queue.push(url);

const TIMEOUT = process.env.TIMEOUT ? parseInt(process.env.TIMEOUT) : 4000;
const DELAY = process.env.DELAY ? parseInt(process.env.DELAY) : 500;

const visit = (url) => {
    let page, browser;
    return new Promise(async (resolve, reject) => {
        try {
            browser = await puppeteer.launch({
                headless: true,
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ],
                dumpio: true,
                executablePath: process.env.PUPPETEER_EXECUTABLE_PATH
            });
            page = await browser.newPage();

            /* load flag */
            await page.goto(process.env.SANDBOX_SITE, {
                waitUntil: "networkidle2"
            });
            await page.evaluate(flag => {
                localStorage.message = flag;
            }, process.env.FLAG);

            await page.goto(url, {
                waitUntil: "networkidle2"
            });
            await page.waitForTimeout(TIMEOUT);
            await page.close();
            page = null;
        } catch (err) {
            console.log(err);
        } finally {
            if (page) await page.close();
            if (browser) await browser.close();
            resolve();
        }
    });
};

const loop = async () => {
    while (true) {
        let url = queue.shift();
        if (url) {
            console.log("vistiting:", url, queue);
            await visit(url);
        }
        await new Promise((resolve, reject) => setTimeout(resolve, DELAY));
    }
};

loop();
module.exports = {
    addToQueue
};