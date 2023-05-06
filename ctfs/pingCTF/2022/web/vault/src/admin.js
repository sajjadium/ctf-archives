const puppeteer = require("puppeteer");

const sleep = async (s) => new Promise((resolve) => setTimeout(resolve, s));

const check = async (url, account_password, password) => {
	let browser;
	try {
		browser = await puppeteer.launch({
			headless: true,
			args: [
				"--disable-gpu",
				"--no-sandbox",
				"--js-flags=--noexpose_wasm,--jitless",
			],
			executablePath: "/usr/bin/chromium-browser",
		});
		const context = await browser.createIncognitoBrowserContext();
		const page = await context.newPage();

		await page.goto("http://127.0.0.1:3000");
		await sleep(500);
		await page.type("[name=login]", "admin");
		await page.type("[name=password]", account_password);
		await page.click("[type=submit]");
		await sleep(4000);

		page.on("dialog", (passDialog) => {
			passDialog.accept(password);
		});

		await page.click("#REVEAL");

		await sleep(1000);
		await page.goto(url);
		await sleep(5000);

		await browser.close();
	} catch (e) {
		console.log(e);
	} finally {
		if (browser) await browser.close();
	}
};

module.exports = { check };
