const puppeteer = require("puppeteer");

const SITE = process.env.SITE || 'http://localhost:8763';
const FLAG = process.env.FLAG || 'test{flag}';

const sleep = async s => new Promise(resolve => setTimeout(resolve, 1000 * s));

const visit = async url => {
	let browser
	try {
		browser = await puppeteer.launch({
			headless: true,
			args: ["--disable-gpu", "--no-sandbox"],
			executablePath: "/usr/bin/chromium-browser",
		});
		const context = await browser.createIncognitoBrowserContext();
		const page = await context.newPage();

		await page.goto(SITE);
		await sleep(1);
		await page.type("textarea[name='message']", FLAG);
		await page.click("#submit");
		await sleep(1);
		await page.waitForSelector("#link");
		const flagUrl = await page.evaluate(() => document.querySelector('#link').textContent);
		console.log(flagUrl);
		console.log(url);
		page.goto(url);
		await sleep(1);
		page.goto(flagUrl);
		await sleep(3);

		await browser.close();

	} catch (e) {
		console.log(e);
	} finally {
		if (browser) await browser.close();
	}

}

module.exports = visit

if (require.main === module) {
	visit('http://localhost:8001/')
}
