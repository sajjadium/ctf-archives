const puppeteer = require('puppeteer');

async function healthCheck(){
  const browser = await puppeteer.launch({
    headless: true,
    args:['--no-sandbox']
  });

  const page = await browser.newPage();
  await page.setJavaScriptEnabled(false)
  const response=await page.goto("http://localhost:3000/view/Healthcheck")
  await browser.close();
}

module.exports = { healthCheck };
