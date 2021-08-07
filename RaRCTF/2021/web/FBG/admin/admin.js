const puppeteer = require("puppeteer");
const path = require("path");

let ext = path.resolve(__dirname, "./extension/");

let queue = [];
const addToQueue = (req) => { queue.push(req); return queue.length };

const TIMEOUT = process.env.TIMEOUT ? parseInt(process.env.TIMEOUT) : 3000;
const DELAY = process.env.DELAY ? parseInt(process.env.DELAY) : 500;

const visit = (req) => {
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
            await page.goto(process.env.SITE, {
                waitUntil: "networkidle2"
            });
            await page.evaluate(flag => {
                localStorage.flag = flag;
            }, process.env.FLAG);

            let url = process.env.SITE + "button?title=" + req.title + "&link=" + req.link;
            console.log("Going to ", url);
            await page.goto(url, {
                waitUntil: "networkidle2"
            });
            await page.click("#btn");
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
        let req = queue.shift();
        if (req) {
            console.log("vistiting:", req, queue);
            await visit(req);
        }
        await new Promise((resolve, reject) => setTimeout(resolve, DELAY));
    }
};

loop();
module.exports = {
    addToQueue
};
