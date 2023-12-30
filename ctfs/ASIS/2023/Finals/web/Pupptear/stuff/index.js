#!/usr/bin/env node
const puppeteer = require('puppeteer')

const flag = 'flag{test-flag}';

async function visit(url){
	let browser;

	if(!/^https?:\/\//.test(url)){
		return;
	}

	try{
		browser = await puppeteer.launch({
		    pipe: true,
		    args: [
		        "--no-sandbox",
		        "--disable-setuid-sandbox",
		        "--js-flags=--noexpose_wasm,--jitless",
		        "--ignore-certificate-errors",
		    ],
		    executablePath: "/usr/bin/google-chrome-stable",
		    headless: 'new'
		});

		let page = await browser.newPage();
		await page.goto(url,{ timeout: 2000 });
		await page.waitForFunction(flag=>{
			let el = document.getElementById('flag')
			if(!el) return false
			el.value = flag
			return true
		},{ timeout: 2000 },flag)
		await new Promise(r=>setTimeout(r,3000));
	}catch(e){}
	try{await browser.close();}catch(e){}
	process.exit(0)
}

visit(atob(process.argv[2]));
