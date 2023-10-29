const puppeteer = require('puppeteer');

const USERNAME = process.env['USERNAME'] || 'admin'
const PASSWORD = process.env['FLAG']

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "http://app/",
    APPURLREGEX: process.env['APPURLREGEX'] || "^.*$",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
    APPLOGINURL: process.env['APPLOGINURL'] || "http://app/login",
}

console.table(CONFIG)

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    headless: 'new',
    args: [
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--no-gpu',
        '--disable-default-apps',
        '--disable-translate',
        '--disable-device-discovery-notifications',
        '--disable-software-rasterizer',
        '--disable-xss-auditor'
    ],
    ipDataDir: '/home/bot/data/',
    ignoreHTTPSErrors: true
});

console.log("Bot started...");

module.exports = {
    name: CONFIG.APPNAME,
    urlRegex: CONFIG.APPURLREGEX,
    rateLimit: {
        windowS: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    bot: async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createIncognitoBrowserContext()
        try {
            // Goto main page
            const page = await context.newPage();
            // login
            console.log('connecting')
            await page.goto(CONFIG.APPLOGINURL, {
                waitUntil: 'networkidle2'
            });
            console.log(page.url())
            await page.waitForSelector('#inputUsername', { timeout: 5000 })
            console.log('username')
            await page.focus('#inputUsername')
            await page.keyboard.type(USERNAME)
            console.log('password')
            await page.focus('#inputPassword')
            await page.keyboard.type(PASSWORD)
            console.log('submit')
            await page.click('#submit')
            console.log('submitted')
            await page.setExtraHTTPHeaders({
                'ngrok-skip-browser-warning':'1'
            })
            // Visit URL from user
            console.log(`bot visiting ${urlToVisit}`)
            await page.goto(urlToVisit, {
                waitUntil: 'networkidle2'
            });
            await page.waitForTimeout(5000);

            // Close
            console.log("browser close...")
            await context.close()
            return true;
        } catch (e) {
            console.error(e);
            await context.close();
            return false;
        }
    }
}
