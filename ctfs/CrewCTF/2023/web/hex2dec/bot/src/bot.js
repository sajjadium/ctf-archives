const puppeteer = require('puppeteer');


const FLAG = process.env.FLAG ?? 'dummy{dummy}';
const APP_HOST = process.env.APP_HOST ?? 'hex2dec-web';
const APP_PORT = process.env.APP_PORT ?? 8084;
const APP_URL = `http://${APP_HOST}:${APP_PORT}/`;

const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const visit = async (v) => {
	console.log(`start: ${v}`);

	const url = new URL(APP_URL);
	url.search = `v=${encodeURIComponent(v)}`;

	const browser = await puppeteer.launch({
	  headless: true,
	  executablePath: '/usr/bin/google-chrome-stable',
	  args: ['--no-sandbox'],
	});

	const context = await browser.createIncognitoBrowserContext();

	const page = await context.newPage();
	await page.setCookie({
	  name: 'FLAG',
	  value: FLAG,
	  domain: `${APP_HOST}:${APP_PORT}`,
	  httpOnly: false
	});

	await page.goto(url, {
		waitUntil: 'networkidle0',
		timeout: 5 * 1000
	});
	await sleep(5 * 1000);
	await page.close();

	await context.close();
	await browser.close();

	console.log(`end: ${url}`);
}

module.exports = { visit: visit };

