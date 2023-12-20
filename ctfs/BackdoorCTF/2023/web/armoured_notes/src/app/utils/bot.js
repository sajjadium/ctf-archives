import puppeteer from 'puppeteer-core';

const CONFIG = {
    APPURL: process.env['APPURL'] ,
    APPURLREGEX: process.env['APPREGEX'] ,
    APPFLAG: process.env['APPFLAG'],
}
console.table(CONFIG)

const initBrowser = puppeteer.launch({
    executablePath: "/usr/bin/google-chrome",
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


const name = CONFIG.APPNAME
 const urlRegex = CONFIG.APPURLREGEX

const bot =  async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createIncognitoBrowserContext()
        try {
            // Goto main page
            const page = await context.newPage();

            // Set Flag
            await page.setCookie({
                name: "flag",
                httpOnly: false,
                value: CONFIG.APPFLAG,
                url: CONFIG.APPURL
            })

            // Visit URL from user
            console.log(`bot visiting ${urlToVisit}`);
            await page.goto(urlToVisit, {
                waitUntil: 'networkidle2'
            });
            await new Promise(resolve => setTimeout(resolve, 5000));

            // Close
            console.log("browser close...");
            await context.close();
            return true;
        } catch (e) {
            console.error(e);
            await context.close();
            return false;
        }
    }
export { bot, urlRegex, name}