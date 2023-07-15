const { chromium } = require('playwright');
const Redis = require('ioredis');
const connection = new Redis(6379, process.env.REDIS_ADDR || "redis");

const BASE_URL = process.env.FRONTEND_BASE_URL || 'http://localhost:8005'
const ADMIN_KEY = process.env.ADMIN_KEY;

const wait = r => new Promise(resolve => {
    setTimeout(resolve, r);
});

const visit = async id => {
    console.log('[+] visit:', id);

    if (!/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}/.test(id)) {
        console.error('[!] id:', id);
        return;
    }

    console.log('[+] started:', id);

    const browser = await chromium.launch({
        args: [
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--js-flags="--noexpose_wasm"'
        ]
    });

    try {
        const context = await browser.newContext();
        const page = await context.newPage();
        await page.setExtraHTTPHeaders({
            'Authorization': ADMIN_KEY
        });

        // let's check the reported post
        const url = `${BASE_URL}/#page=post&id=${id}&admin=yes`;
        await page.goto(url);
        await page.waitForSelector('.like', { timeout: 5000 });

        // click the first like button
        await page.click('.like');

        // done!
        await wait(1000);

        await context.close();
    } catch (e) {
        console.error(e);
    }

    await browser.close();

    console.log('[+] done:', id);
};

const handle = async () => {
    console.log(await connection.ping());
    connection.blpop('report', 0, async (err, message) => {
        try {
            await visit(message[1]);
            setTimeout(handle, 10);
        } catch (e) {
            console.log("[-] " + e);
        }
    });
};

console.log('[+] running');
handle();
