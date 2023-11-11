const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis(6379, process.env.REDIS_HOST || "redis", {db: 1});

const flag = process.env.flag || "FakeCTF{**** DUMMY FLAG *****}";
const base_url = "http://challenge:8080";
const browser_option = {
    executablePath: '/usr/bin/google-chrome',
    headless: "new",
    args: [
        '-wait-for-browser',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--js-flags="--noexpose_wasm"'
    ]
}

const crawl = async (target) => {
    const url = `${base_url}/${target}`;
    console.log(`[+] Crawling: ${url}`);

    const browser = await puppeteer.launch(browser_option);
    const page = await browser.newPage();
    try {
        await page.setCookie({
            name: 'flag',
            value: flag,
            domain: new URL(base_url).hostname,
            httpOnly: false,
            secure: false
        });
        await page.goto(url, {
            waitUntil: 'networkidle0',
            timeout: 3 * 1000,
        });
        await page.waitForTimeout(3 * 1000);
    } catch (e) {
        console.log("[-]", e);
    } finally {
        await page.close();
        await browser.close();
    }
}

const handle = async () => {
    console.log(await connection.ping());
    connection.blpop('report', 0, async (err, message) => {
        try {
            await crawl(message[1]);
            setTimeout(handle, 10);
        } catch (e) {
            console.log("[-] " + e);
        }
    });
};

handle();
