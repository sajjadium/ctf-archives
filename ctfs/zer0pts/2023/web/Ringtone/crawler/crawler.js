const puppeteer = require('puppeteer');
const Redis = require('ioredis');
const connection = new Redis(6379, process.env.REDIS_HOST || "redis", {db: 1});

const flagPath = process.env.RANDOM || "REDACTED"
const base_url ="http://challenge:8080";
const browser_option = {
    executablePath: '/usr/bin/google-chrome',
    headless: false,
    ignoreHTTPSErrors: true,
    args: [
        "--no-sandbox",
        "--load-extension=/extension",
        "--disable-extensions-except=/extension",
        "--enable-automation"
    ]
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

const crawl = async (target) => {
    const url = `${base_url}/${target}`;
    console.log(`[+] Crawling: ${url}`);
    const flagUrl=`${base_url}/${flagPath}`;
    const extUrl="chrome-extension://pifcfidoojbiodholilemccdnkcibghf/index.html"
    const browser = await puppeteer.launch(browser_option);
    
    const page2 = await browser.newPage();
    await page2.goto(base_url, {
            waitUntil: 'networkidle0',
            timeout: 2 * 1000,
        });
    const pageExt=await browser.newPage();
    await pageExt.goto(extUrl);
    await sleep(1000)
    const page1 = await browser.newPage();
    await page1.goto(flagUrl);
    await page1.close();
    const page = await browser.newPage();
    await page.goto(url, {
            waitUntil: 'networkidle0',
            timeout: 3 * 1000,
        });
  //  await page.close();
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
