#!/usr/bin/env node
const puppeteer = require('puppeteer');

(async () => {
	const opts = JSON.parse(atob(process.argv[2]))

	let browser
	try {		
		browser = await puppeteer.launch({
		    headless: 'chrome',
		    pipe: true,
		    args: [
		        "--no-sandbox",
		        "--disable-setuid-sandbox",
		        "--js-flags=--noexpose_wasm,--jitless",
		    ],
		    executablePath: "/usr/bin/google-chrome",
		});

		console.log('[+] Browser online')

		let page = await browser.newPage();
		await page.goto(opts.url.toString(), { timeout: 3000, waitUntil: 'domcontentloaded' });

		let ackCnt = Math.min(10,+opts.actions.length)
		for(let i=0;i<ackCnt;i++){
			let pages = await browser.pages()
			let idx = opts.actions[i].pageIdx
			let payload = opts.actions[i].payload.toString()

			await pages[idx].evaluate((s)=>eval(s),payload)
			await new Promise((r)=>setTimeout(r,300));
			console.log(`[+] Executed payload ${i}`)
		}

		await page.close();
		await browser.close();
		browser = null;
    } catch(err){
    } finally {
        if (browser) await browser.close();
		console.log(`[+] Browser closed`)
    }
})();


