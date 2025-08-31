import puppeteer from 'puppeteer-core';
import { spawn, exec } from 'child_process';

let PORT = 9999;

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
	exec(`kill -9 $(ps aux | grep 'remote-debugging-port=${PORT}' | awk '{print $2}')`)

	const child = spawn('/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome',
		['--headless', '--disable-gpu', `--remote-debugging-port=${PORT}`]);

	await delay(1000);

    const response = await fetch(`http://localhost:${PORT}/json/version`);

    const conn = await response.json();

	const browser = await puppeteer.connect({
		browserWSEndpoint: conn.webSocketDebuggerUrl
	});

	const page = await browser.newPage();
	await page.goto(process.argv[2], { waitUntil: 'networkidle0' });

	console.log(await page.content());

	await browser.close();
})();
