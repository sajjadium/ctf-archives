const crypto = require('crypto');
const { chromium } = require('playwright');
const Redis = require('ioredis');
const connection = new Redis(6379, process.env.REDIS_ADDR || "redis", {db: 0});

const BASE_URL = process.env.BASE_URL || 'http://localhost:8005'
const FLAG = process.env.FLAG || 'nek0pts{DUMMY}';
const MASTER_KEY = process.env.MASTER_KEY;

const wait = r => new Promise(resolve => {
    setTimeout(resolve, r);
});

const visit = async id => {
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(id)) {
        console.error('[!] id:', id);
        return;
    }

    console.log('[+] started:', id);

    const browser = await chromium.launch({
        headless: false,
        args: [
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--js-flags="--noexpose_wasm"'
        ]
    });

    try {
        const context = await browser.newContext();
        const page = await context.newPage();
    
        // post a note that has the flag
        await page.goto(`${BASE_URL}/`);
    
        await page.type('#title', 'Flag');
        await page.type('#body', `The flag is: ${FLAG}`);
        const password = crypto.randomBytes(64).toString('base64');
        await page.type('#password', password);
    
        await page.click('#submit');
    
        // let's check the reported note
        await page.goto(`${BASE_URL}/note/${id}`);
        if (await page.$('input') != null) {
            // the note is locked, so use master key to unlock
            await page.type('input', MASTER_KEY);
            await page.click('button');
    
            // just in case there is a vuln like XSS, delete the password to prevent it from being stolen
            const len = (await page.$eval('input', el => el.value)).length;
            await page.focus('input');
            for (let i = 0; i < len; i++) {
                await page.keyboard.press('Backspace');
            }
        }
    
        // it's ready now. click "Show the note" button
        await page.click('button');
    
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
