const Redis = require("ioredis")
const puppeteer = require("puppeteer")
const dotenv = require('dotenv')

dotenv.config()

const USERNAME = 'admin';
const PASSWORD = process.env.ADMIN_PASSWORD;
const BASE_URL = process.env.CRAWL_ORIGIN;
const REDIS_HOST = process.env.REDIS_HOST || 'localhost';
const REDIS_PORT = 6379;
const REDIS_PASSWORD = process.env.REDIS_PASSWORD;
const TIMEOUT = 5000;

const redis = new Redis({
    host: REDIS_HOST,
    port: REDIS_PORT,
    password: REDIS_PASSWORD
})

let browser;
let page;

const crawl = async (path) => {
    try {
        page = await browser.newPage()
        
        await page.goto(BASE_URL + path, {
            waitUntil: "networkidle2",
            timeout: TIMEOUT,
        })
        await page.close()
    } catch(e) {
        console.log(`[*] error(${path}): ${e}`)
    }
}

(async () => {
    browser = await puppeteer.launch({
        headless: true,
        executablePath: process.env.PUPPETEER_EXECUTABLE_PATH,
        args: [
          "--no-sandbox",
          "--disable-background-networking",
          "--disk-cache-dir=/dev/null",
          "--disable-default-apps",
          "--disable-extensions",
          "--disable-desktop-notifications",
          "--disable-gpu",
          "--disable-sync",
          "--disable-translate",
          "--disable-dev-shm-usage",
          "--hide-scrollbars",
          "--metrics-recording-only",
          "--mute-audio",
          "--no-first-run",
          "--safebrowsing-disable-auto-update",
          "--window-size=1440,900",
        ],
    });
    page = await browser.newPage()

    await page.goto(BASE_URL + "/login", {
        waitUntil: "networkidle2",
        timeout: 3000,
    });

    await page.type('input[id="username"]', USERNAME)
    await page.type('input[id="password"]', PASSWORD)

    await Promise.all([
        page.click('button[id="loginButton"]'),
        page.waitForNavigation({
            waitUntil: "networkidle2",
            timeout: TIMEOUT,
        })
    ])
    
    while (true) {
        console.log(
            "[*] progress: ",
            await redis.get("proceeded_report_count"),
            "/",
            await redis.get("reported_count")
        )
        await redis
            .blpop("report", 0)
            .then((v) => {
                const path = v[1];
                console.log(`[*] crawl ${path}`)
                return crawl(path)
            })
            .then(() => {
                return redis.incr("proceeded_report_count")
            })
    }
})()