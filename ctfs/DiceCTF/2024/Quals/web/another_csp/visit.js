import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
	pipe: true,
	args: [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--js-flags=--noexpose_wasm,--jitless',
		'--incognito'
	],
	dumpio: true,
	headless: 'new'
});

const [token, code] = process.argv.slice(2);

try {
	const page = await browser.newPage();
	await page.goto('http://127.0.0.1:8080');
	await page.evaluate((token, code) => {
		localStorage.setItem('token', token);
		document.getElementById('code').value = code;
	}, token, code);
	await page.click('#submit');
	await page.waitForFrame(frame => frame.name() == 'sandbox', { timeout: 1000 });
	await page.close();
} catch(e) {
	console.error(e);
};

await browser.close();