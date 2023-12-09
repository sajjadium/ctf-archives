var puppeteer = require("puppeteer");

const FLAG = process.env.FLAG ?? "ping{FAKE}";

module.exports = async (url) => {
	const browser = await puppeteer.launch({
		headless: "new",
		pipe: true,
		args: [
			"--disable-gpu",
			"--no-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		],
		executablePath: "/usr/bin/chromium-browser",
	});

	const page = await browser.newPage();
	await page.setCookie({
		name: "FLAG",
		value: FLAG,
		domain: "localhost",
		path: "/",
	});

	await page.goto(url);

	await new Promise((resolve) => setTimeout(resolve, 3000));

	await browser.close();
};
