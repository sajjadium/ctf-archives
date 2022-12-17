const puppeteer = require("puppeteer");

const sleep = async (s) => new Promise((resolve) => setTimeout(resolve, s));

const check = async (noteId, password) => {
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

		page.once("dialog", (loginDialog) => {
			loginDialog.accept("admin");
			page.once("dialog", (passwordDialog) => {
				passwordDialog.accept(password);
			});
		});

		await page.goto(`http://127.0.0.1:3000/view.html?id=${noteId}`);

		await sleep(5000);

		await browser.close();
	} catch (e) {
		console.log(e);
	} finally {
		if (browser) await browser.close();
	}
};

module.exports = { check };
