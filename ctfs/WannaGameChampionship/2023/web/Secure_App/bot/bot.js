const fs = require('node:fs');

flag = fs.readFileSync('/flag', 'utf8');

const puppeteer = require('puppeteer');

const browser_options = {
	headless: "new",
	args: [
		'--no-sandbox',
		'--disable-background-networking',
		'--disable-default-apps',
		'--disable-extensions',
		'--disable-gpu',
		'--disable-sync',
		'--disable-translate',
		'--hide-scrollbars',
		'--metrics-recording-only',
		'--mute-audio',
		'--no-first-run',
		'--safebrowsing-disable-auto-update',
		'--js-flags=--noexpose_wasm,--jitless',
		'--unsafely-treat-insecure-origin-as-secure=http://app:80'
	]
};

const visitPage = async url => {
	const browser = await puppeteer.launch(browser_options);
	let context = await browser.createIncognitoBrowserContext();
	let page = await context.newPage();

    await page.goto('http://app:80/login.php');
    await page.type('[name="username"]', 'admin');	
    await page.type('[name="password"]', flag);
    await Promise.all([
        page.click('[type="submit"]'),
        page.waitForNavigation({ waituntil: 'domcontentloaded' })
    ]);

	await page.goto(url, {
		waitUntil: 'networkidle2',
		timeout: 5000
	});


	// for safe
	await page.goto('http://app:80/api/logout.php');
	await page.type('[name="confirm_code"]', flag);
    await Promise.all([
        page.click('[type="submit"]'),
        page.waitForNavigation({ waituntil: 'domcontentloaded' })
    ]);

	await browser.close();
};

module.exports = { visitPage };