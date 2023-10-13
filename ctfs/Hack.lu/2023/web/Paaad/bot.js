const puppeteer = require('puppeteer');
const crypto = require('crypto')

const TIMEOUT_SECS = parseInt(process.env.TIMEOUT_SECS || '30', 10);
const DOMAIN = process.env.DOMAIN || console.log('URL missing Wtf')
const FLAG = process.env.FLAG || console.log('FLAG missing Wtf')
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || console.log('ADMIN_USERNAME missing Wtf')
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || console.log('ADMIN_PASS missing Wtf')


if (process.argv.length !== 3 && process.argv.length !== 4) {
    console.log(`Usage: node ${process.argv[1]} <url> [cookies]`);
    process.exit(1);
  }

const padid = process.argv[2];
const cookies = JSON.parse(process.argv[3] || '[]');

const setCookies = async (cookies, page) => {
    // set the cookies from json 
    for (const cookieSite of cookies) {
        console.log('[Cookie]', 'Visiting', cookieSite.url);
        await page.goto(cookieSite.url);
        console.log('[Cookie]', 'Setting cookies:', ...cookieSite.cookies);
        await page.setCookie(...cookieSite.cookies);
    }
};


if (!padid || padid === '' || typeof (padid) !== 'string' || !/^[a-f0-9]{48}$/.test(padid) ) {
    console.log('No URL provided!');
    process.exit(1);
}

(async () => {
    // launch a browser with our config
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: "/usr/bin/chromium-browser",
        args: [
            // disable stuff we do not need
            '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage',
            // disable sandbox since it does not work inside docker
            // (but we will use seccomp at least)
            '--no-sandbox',
            // no exploits please
            "--js-flags=--noexpose_wasm,--jitless",
        ],
    });

    // close the browser after TIMEOUT_SECS seconds
    setTimeout(() => {
        console.log('Timeout reached, closing browser');
        browser.close()
    }, TIMEOUT_SECS * 1000
    );

    // open a new page
    let page = await browser.newPage();

    // login 
    await page.goto(`https://${DOMAIN}/user/login`, { waitUntil: 'networkidle0' }); // wait until page load
    // generate admin creds
    await page.type('#username', ADMIN_USERNAME);
    await page.type('#password', ADMIN_PASSWORD);
    // click and wait for navigation
    await Promise.all([
        page.click('#submit'),
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
    ]);

    // create flag pad
    await page.goto(`https://${DOMAIN}/p/new`, { waitUntil: 'networkidle0' }); // wait until page load
    await page.type('#title', 'flag');
    await page.type('#content', FLAG);
    // click and wait for navigation
    await Promise.all([
        page.click('#submit'),
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
    ])


    // avoid leaking anything
    await page.close();
    page = await browser.newPage();

    page.on('console', (msg) => {
        console.log('[Console]', msg);
    });

    // open the link
    console.log(`Visiting URL: https://${padid}.${DOMAIN} `);
    await page.goto(`https://${padid}.${DOMAIN}`);
})().catch(error => {
    console.log('Error:', error);
    process.exit(1);
});
