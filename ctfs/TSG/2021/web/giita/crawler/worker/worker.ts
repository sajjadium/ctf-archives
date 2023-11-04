import puppeteer from 'puppeteer';
import Redis from 'ioredis';

const connection = new Redis(6379, 'redis');

const browserOption = {
	executablePath: 'google-chrome-stable',
	headless: true,
	args: [
		'--no-sandbox',
		'--disable-background-networking',
		'--disk-cache-dir=/dev/null',
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
	],
};

const crawl = async (url: string) => {
	console.log(`[*] started: ${url}`)

	const browser = await puppeteer.launch(browserOption);
	const page = await browser.newPage();
	await page.setCookie({
		name: 'cookie',
		value: process.env.FLAG!,
		domain: process.env.DOMAIN!,
		expires: Date.now() / 1000 + 10,
	});
	await page.setExtraHTTPHeaders({
		'Bypass-Tunnel-Reminder': 'true',
	});
	try {
		await page.goto(url, {
			waitUntil: 'load',
			timeout: 10000,
		});
	} catch (err) {
		console.error(err);
	}
	await page.close();
	await browser.close();
	console.log(`[*] finished: ${url}`)
};

// handle the whole
const handle = () => {
	console.log('[*] waiting new query ...')
	connection.blpop('query', 0, async (err, message) => {
		if (err) {
			console.error(err);
			return;
		}
		const url = message[1];
		await crawl(url);
		await connection.incr("proceeded_count");
		setTimeout(handle, 10);
	});
}

handle();
