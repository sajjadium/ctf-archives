const puppeteer = require('puppeteer');

const browser_options = {
    headless: false,
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
		'--js-flags=--noexpose_wasm,--jitless'
	]
};

const visitPage = async url => {
	const browser = await puppeteer.launch(browser_options);

	let context = await browser.createIncognitoBrowserContext();
	let page = await context.newPage();

    await page.goto('http://127.0.0.1:8001/login.php');
    await page.type('[name="username"]', 'admin');	
    await page.type('[name="password"]', 'adminto^password');
    await Promise.all([
        page.click('[type="submit"]'),
        page.waitForNavigation({ waituntil: 'domcontentloaded' })
    ]);

	await page.goto(url, {
		waitUntil: 'networkidle2'
	});

	await page.waitForTimeout(2000);

	// for safe
	await page.goto('http://127.0.0.1:8001/api/logout.php');
	await page.type('[name="confirm_code"]', 'adminto^password');
    await Promise.all([
        page.click('[type="submit"]'),
        page.waitForNavigation({ waituntil: 'domcontentloaded' })
    ]);
	// Close the browser
	await browser.close();

	await browser.close();
};

visitPage('http://s6y6ai72.requestrepo.com')