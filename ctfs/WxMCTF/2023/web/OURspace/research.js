const puppeteer = require('puppeteer');
const fs = require('fs');

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const FLAG = process.env.FLAG ?? "wxmctf{dummy_flag}";

module.exports.research = async (url) => {
    if (fs.existsSync('./image.png')) {
        fs.rmSync('./image.png');
    }
    const browser = await puppeteer.launch({
        headless: true
    });
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:3000/');
    await page.setCookie({ name: 'flag', value: FLAG });
    await sleep(200);
    await page.goto('about:blank');
    await page.setViewport({ width: 800, height: 400 });
    await sleep(500);
    await page.setRequestInterception(true);
    page.on('request', (intercept) => {
        let url = new URL(intercept.url());
        if (["http:", "https:"].includes(url.protocol) && url.hostname != '127.0.0.1') {
            intercept.abort();
        }
        else {
            intercept.continue();
        }
    })
    await page.goto(url, { waitUntil: 'networkidle0' }).catch(() => {
        // :p
    });
    await sleep(1000);
    await page.screenshot({ path: './image.png' });
    await sleep(2000);
    await browser.close().then(() => {
        writeToFile();
    }).catch(() => writeToFile());
}

function writeToFile() {
    let status = JSON.parse(fs.readFileSync('./status.json').toString());
    status.visiting = false;
    fs.writeFileSync('./status.json', JSON.stringify(status));
}
