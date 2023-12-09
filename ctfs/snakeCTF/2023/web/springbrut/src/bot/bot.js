const puppeteer = require('puppeteer');
const net = require('net');
const WEBSITE = process.env['WEBSITE'] || 'http://springbrut:8080'

const LOGIN_PAGE = WEBSITE + "/login"
const ADMIN_USERNAME = "admin"
const ADMIN_PASSWORD = process.env['ADMIN_PASSWORD'] || "admin"

console.log(`Starting admin bot!`);

(async () => {
    const doAdmin = async () => {
        const browser = await puppeteer.launch({
            //executablePath: '/usr/bin/google-chrome-stable',
            headless: true,
            dumpio: true,
            args: [
                '--no-sandbox',
                '--disable-background-networking',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-gpu',
                '--disable-sync',
                '--disable-translate',
                '--hide-scrollbars',
                '--metrics-recording-only',
                '--mute-audio',
                '--no-first-run',
                '--safebrowsing-disable-auto-update'
                //'--enable-logging=stderr',
            ]
        });
        try {
            var context = await browser.createIncognitoBrowserContext();
            var page = await context.newPage();
            console.log('logging in and checking status');
            await page.goto(LOGIN_PAGE, { waitUntil: "networkidle2" });
            console.log('Waiting for username');
            await page.waitForSelector('input[name="username"]');
            console.log('Typing username');
            await page.type('input[name="username"]', ADMIN_USERNAME, {
                delay: 5,
            });
            console.log('Waiting for password');
            await page.waitForSelector('input[name="password"]');
            console.log('Typing for password');
            await page.type('input[name="password"]', ADMIN_PASSWORD, {
                delay: 5,
            });
            console.log('Waiting for submit');
            await page.waitForSelector('button[type="submit"]');
            console.log('Clicking submit');
            await page.click('button[type="submit"]');
            console.log('Waiting for page load');
            await page.waitForNetworkIdle(3000);
            console.log('Login successful, waiting a bit :)');
            await page.waitForTimeout(3000);
            console.log('Cleaning up mess');
            await page.close();
            await context.close();
        } catch (err) {
            console.log('Error occurred');
            console.log(err);
        }
        await browser.close();
    }
    setTimeout(doAdmin, 5000);
    setInterval(doAdmin, 60000);
}
)();
