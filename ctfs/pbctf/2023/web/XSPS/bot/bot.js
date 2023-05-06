const redis = require('redis');
const r = redis.createClient({
    socket: {
        port      : 6379,               // replace with your port
        host      : 'redis',        // replace with your hostanme or IP address
    }})

const puppeteer = require('puppeteer');

async function browse(url){

    console.log(`Browsing -> ${url}`);
    const browser = await (await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-gpu'],
        executablePath: "/usr/bin/google-chrome"
    })).createIncognitoBrowserContext();

    const page = await browser.newPage();
    await page.setCookie({
        name: 'session',
        value: process.env.CHALL_COOKIE,
        domain: process.env.CHALL_HOST
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
