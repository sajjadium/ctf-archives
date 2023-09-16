const puppeteer = require('puppeteer');

const ADMIN_TOKEN = process.env.ADMIN_TOKEN ?? console.log('No admin token') ?? process.exit(1);

const APP_HOST = 'localhost';
const APP_PORT = '3000';

const sleep = async (msec) => new Promise((resolve) => setTimeout(resolve, msec));

const visit = async (url) => {
  console.log(`start: ${url}`);

  const browser = await puppeteer.launch({
    headless: "new",
    executablePath: '/usr/bin/google-chrome-stable',
    args: ['--no-sandbox'],
  });

  const context = await browser.createIncognitoBrowserContext();
  try {
    const page = await context.newPage();
    await page.setCookie({
      name: 'token',
      value: ADMIN_TOKEN,
      domain: `${APP_HOST}:${APP_PORT}`,
      httpOnly: true
    });
    await page.goto(url, { timeout: 3 * 1000 });
    await sleep(3 * 1000);
    await page.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`end: ${url}`);
};

module.exports = { visit }
