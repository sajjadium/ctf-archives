const redis = require('redis');
const r = redis.createClient({
    port      : 6379,               // replace with your port
    host      : 'redis',        // replace with your hostanme or IP address
})

const puppeteer = require('puppeteer');

async function browse(url){

    console.log(`Browsing -> ${url}`);
    const browser = await (await puppeteer.launch({
        headless: true,
    args: ['--no-sandbox', '--disable-gpu']
    })).createIncognitoBrowserContext();

    const page = await browser.newPage();
    await page.setCookie({
        name: 'session',
        value: process.env.CHALL_COOKIE,
        domain: process.env.CHALL_HOST,
        sameSite: "Lax",
        secure: true,
    });

    try {
        const resp = await page.goto(url, {
            waitUntil: 'load',
            timeout: 20 * 1000,
        });
    } catch (err){
        console.log(err);
    }

    await page.close();
    await browser.close();

    console.log(`Done visiting -> ${url}`)

}

function main() {
    r.blpop(['submissions', 0], async (_, submit_url) => {
        let url = submit_url[1];
        await browse(url);
        main();
    }); 
}


console.log("XSS Bot ready");
main()
