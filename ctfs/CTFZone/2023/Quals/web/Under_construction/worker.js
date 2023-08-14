const { workerData, parentPort } = require('worker_threads')
const puppeteer = require('puppeteer');

const puppeter_args = {
    headless: "new",
    args: [
      '--headless=new',
      '--block-new-web-contents',
      '--disable-popup-blocking=false',
      '--no-sandbox'
    ]
  };

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function visitUrl(site_url)
  {
    try {
      const browser = await puppeteer.launch(puppeter_args);
      const context = await browser.createIncognitoBrowserContext();
      const page = await context.newPage();
      await page.goto(site_url);
      await sleep(5000);
      await context.close();
    } catch (error) {
      console.log(error);
    }

  }

console.log('Worker url:' + workerData);
visitUrl(workerData)