const redis = require('redis');
const REDIS_PASSWORD = process.env.REDIS_PASSWORD ? process.env.REDIS_PASSWORD: "redis_password"
const REDIS_URL = `redis://:${REDIS_PASSWORD}@localhost:6379`

console.log("redis url",REDIS_URL)

const r = redis.createClient({
    url: REDIS_URL,
})

const puppeteer = require('puppeteer');

async function browse(url) {
    let browser, admin_login_page, new_page;
    try {

        console.log(`Browsing -> ${url}`);

        browser = await (await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-gpu', '--disable-setuid-sandbox', '--js-flags=--noexpose_wasm,--jitless']
        }))
        const browse_time_seconds = process.env.BROWSE_TIME ? parseInt(process.env.BROWSE_TIME) : 15
        const admin_password = process.env.ADMIN_PASSWORD ? process.env.ADMIN_PASSWORD : 'password'

        admin_login_page = await browser.newPage();

        await admin_login_page.goto(
            "http://localhost:12345/login"
        )

        await admin_login_page.type('[name="user"]', "admin", {
            delay: 100,
        });

        await admin_login_page.type('[name="pass"]', admin_password, {
            delay: 100,
        });

        await admin_login_page.click('[type="submit"]');

        await admin_login_page.close();

        new_page = await browser.newPage()

        await new_page.goto(url)

        await new Promise((resolve) => setTimeout(resolve, browse_time_seconds * 1000));

        // await new_page.close()

        await browser.close();

        console.log(`Done visiting -> ${url}`)

        browser = null
        admin_login_page = null
        new_page = null

    } catch (e) {
        console.log("exceptions occur ", e)
    } finally {
        if (browser) await browser.close()
    }

}

async function main() {
    let url = (await r.blPop(redis.commandOptions({isolated: true}),
        'submissions',
        0)).element
    await browse(url)
    main()
}


console.log("XSS Bot ready");
r.connect()
main()
