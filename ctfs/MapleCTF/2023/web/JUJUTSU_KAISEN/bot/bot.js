const redis = require('redis');

const CHALL_DOMAIN = process.env.CHALL_DOMAIN || "https://nginx:443";
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || "placeholder";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "placeholder";
const REDISHOST = process.env.redishost || 'redis';

const r = redis.createClient({
    socket: {
        port      : 6379,               // replace with your port
        host      : REDISHOST,        // replace with your hostanme or IP address
    }})

const puppeteer = require('puppeteer');

async function browse(url){

    console.log(`Browsing -> ${url}`);
    const browser = await (await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox', 
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-setuid-sandbox',
            '--ignore-certificate-errors',
        ],
        executablePath: "/usr/bin/google-chrome",
    })).createIncognitoBrowserContext();

    const loginPage = await browser.newPage();
    const page = await browser.newPage();
    try {
        await loginPage.goto(`${CHALL_DOMAIN}/login`, {
            waitUntil: 'networkidle2',
            timeout: 2 * 1000,
        });
        await loginPage.type('#username', ADMIN_USERNAME);
        await loginPage.type('#password', ADMIN_PASSWORD);
        await loginPage.evaluate(() => {
            document.querySelector("#submit-login").click();
        });
        await loginPage.waitForNavigation({
            waitUntil: 'networkidle2',
            timeout: 2 * 1000,
        });

        const resp = await page.goto(url, {
            waitUntil: 'load',
            timeout: 3 * 1000,
        });
        await new Promise((resolve) => setTimeout(resolve, 60 * 1000));
        await page.close();
        await loginPage.close();
    } catch (err){
        console.log(err);
    } finally {
    }
    await browser.close();


    console.log(`Done visiting -> ${url}`)
    return;
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

async function main() {
  try {
    const submit_url = await r.blPop(
      redis.commandOptions({ isolated: true }),
      "submissions",
      0
    );
    let url = submit_url.element;
    await browse(url);
  } catch (e) {
    console.log("error");
    console.log(e);
  }
  main();
}

async function conn(){
    await r.connect();
}

console.log("XSS Bot ready");
conn();
main()
