#!/usr/bin/env node
const puppeteer = require('puppeteer');

(async () => {
	const url = atob(process.argv[2])

	let browser
	try {		

		browser = await puppeteer.launch({
		    headless: false,
		    pipe: true,
		    executablePath: "/usr/bin/google-chrome-stable",
		});

		console.log('[+] Browser online')

		let page = await browser.newPage()
		await page.goto('file:///flag.txt', { timeout: 3000, waitUntil: 'domcontentloaded' })
		await page.evaluate(()=>{
			const selection = window.getSelection();
			const range = document.createRange();
			range.selectNode(document.querySelector("body > pre"))
			selection.addRange(range);
			document.execCommand('copy')
		})
		await page.close()

		if(/^https?:\/\//.test(url)){
			page = await browser.newPage()
			await page.goto(url);
			await new Promise((r)=>setTimeout(r,3000));
		}

		await page.close()
		await browser.close()
		browser = null
    } catch(err){
    } finally {
        if (browser) await browser.close()
		console.log(`[+] Browser closed`)
    }
})();

