const puppeteer = require("puppeteer");

const ADMIN_PASS = process.env.ADMIN_PASS || 'password';
const login_url = 'http://localhost:1337/login';

const browser_options = {
        headless: true,
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
        ],
	ignoreHTTPSErrors: true
};

async function visit_page(url) {
	console.log(`visiting ${url}...`);
	const browser = await puppeteer.launch(browser_options);
	const page = await browser.newPage();
	
	await page.goto(login_url);
	await page.type('input[name="username"]', 'admin');
	await page.type('input[name="password"]', ADMIN_PASS);
	await Promise.all([
		page.waitForNavigation(),
		page.click('input[name="login"]')

	]);
	try{
	await page.goto(url, {waitUntil: 'networkidle2', timeout: 30000});
	}catch{
		console.log('failed!');
		process.exit(1);
	;}
}

const url = process.argv[2];

visit_page(url);
