// adminbot test script
// npm i puppeteer

const puppeteer = require("puppeteer");

const TEST_USER = "aaaaaaaaaaa";
const TEST_PASS = "bbbbbbbbbbb";
const EXPLOIT_URL = "https://example.com";

function sleep(time) {
    return new Promise(resolve => {
        setTimeout(resolve, time)
    })
}

async function visit(url) {
    const browser = await puppeteer.launch({
        dumpio: true,
        pipe: true,
        args: ["--js-flags=--noexpose_wasm,--jitless"],
        headless: "new"
    });
    const ctx = await browser.createIncognitoBrowserContext();
    const page = await ctx.newPage();

    await page.goto("https://leaklessnote.chals.sekai.team/login.php", { waitUntil: 'domcontentloaded' });
    await sleep(2000);

    await page.type("input[name=name]", TEST_USER);
    await page.type("input[name=pass]", TEST_PASS);
    await page.click("input[type=submit]");
    await sleep(2000);

    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await sleep(65000);
    await browser.close();
}

visit(EXPLOIT_URL);
