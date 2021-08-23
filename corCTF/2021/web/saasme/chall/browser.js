const puppeteer = require('puppeteer');

const url = process.argv[2];

async function main() {
	const browser = await puppeteer.launch({
		headless: true,
		dumpio: true,
		args: ['--no-sandbox'],
		executablePath: '/code/chromium/chrome'
	});
	const page = await browser.newPage();
	await page.setDefaultNavigationTimeout(45 * 1000);
	await page.goto(url);
}

main();