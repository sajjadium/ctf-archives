const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis({
    host: process.env.REDIS_HOST || '127.0.0.1',
    port: process.env.REDIS_PORT || 6379,
    password: process.env.REDIS_PASSWORD || ''
});

const flag = process.env.FLAG || 'linectf{dummy}';
const browser_option = {
    headless: false,
    args: [
        "--no-sandbox",
        "--disable-background-networking",
        "--disk-cache-dir=/dev/null",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-desktop-notifications",
        "--disable-gpu",
        "--disable-popup-blocking",
        "--disable-sync",
        "--disable-translate",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        "--metrics-recording-only",
        "--mute-audio",
        "--no-first-run",
        "--safebrowsing-disable-auto-update"
    ]
}

let browser = undefined;

const init = async () => {
    const browser = await puppeteer.launch(browser_option);
    return browser;
};

const timeout = async (ms) => new Promise((_, reject) => setTimeout(reject, ms));

const crawl = async (url) => {
    console.log(`[+] Crawling started: ${url}`);

    const page = await browser.newPage();
    try {
        const checkNote = async () => {
            await page.setCookie({
                name: 'flag',
                value: flag,
                domain: 'nginx',
                httpOnly: false,
                secure: false
            });
            await page.goto(process.env.BASE_URL, {
                waitUntil: 'networkidle0',
                timeout: 3 * 1000,
            })

            // login
            userIdSelector = '#inputUserId'
            passwordSelector = '#inputPassword'
            await page.waitForSelector(userIdSelector);
            await page.type(userIdSelector, process.env.ADMIN_USER_ID || 'admin');
            await page.waitForSelector(passwordSelector);
            await page.type(passwordSelector, process.env.ADMIN_PASSWORD || 'P@ssw0rd');
            await Promise.all([
                page.waitForNavigation(),
                page.click('button[type=submit]')
            ]);

            // check shared note
            await page.goto(url, {
                waitUntil: 'networkidle0',
                timeout: 3 * 1000,
            });
            printInfoBtnSelector = '#printInfoBtn'
            await page.waitForSelector(printInfoBtnSelector);
            await page.click(printInfoBtnSelector);
        }
        await Promise.race([checkNote(), timeout(15 * 1000)])
    } catch (e) {
        console.log('[-] ERROR');
        console.log('[-]', e);
    } finally {
        await page.close();
        console.log(`[+] Crawling finished: ${url}`);
    }
};

const handle = () => {
    console.log('[+] handle');
    connection.blpop('query', 0, async (err, message) => {
        try {
            browser = await init();
            await crawl(message[1]);
            await browser.close();
            setTimeout(handle, 10);
        } catch (e) {
            console.log(e)
        }
    });
};

handle();
