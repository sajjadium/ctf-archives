const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis(6379, process.env.REDIS_HOST || "redis", {db: 1});

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
const flag = process.env.flag || "CakeCTF{**** TEST FLAG *****}";
const base_url = "http://challenge:8080";
const browser_option = {
    headless: true,
    args: [
        '-wait-for-browser',
        '--no-sandbox', '--disable-gpu',
        '--js-flags="--noexpose_wasm"'
    ]
}

const crawl = async (target) => {
    const url = base_url + '/profile/' + target + '?report';
    console.log(`[+] Crawling: ${url}`);

    const username = Math.random().toString(32).substring(2);
    const password = Math.random().toString(32).substring(2);

    const browser = await puppeteer.launch(browser_option);
    try {
        const page = await browser.newPage();
        // Register
        await page.goto(base_url + '/', {timeout: 3000});
        await page.type('#username', username);
        await page.type('#password', password);
        await page.click('#tab-signup');
        await page.click('#signup');
        await wait(1000);

        // Set flag to bio
        await page.goto(base_url + '/', {timeout: 3000});
        await page.$eval('#bio', element => element.value = '');
        await page.type('#bio', "You hacked me! The flag is " + flag);
        await page.click('#update');
        await wait(1000);

        // Check spam page
        await page.goto(url, {timeout: 3000});
        await wait(3000);
        await page.close();
    } catch(e) {
        console.log("[-] " + e);
    }

    console.log(`[+] Crawl done`);
    await browser.close();
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
