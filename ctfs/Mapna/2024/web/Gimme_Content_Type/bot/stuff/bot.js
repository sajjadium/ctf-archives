#!/usr/bin/env node
const puppeteer = require('puppeteer')

async function visit(stuff){
	let browser;

	let url = stuff['url'];
	let flag = stuff['flag'];

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
		        '--unsafely-treat-insecure-origin-as-secure=http://web:8000'
		    ],
		    executablePath: "/usr/bin/google-chrome-stable",
		    headless: 'new'
		});

		let page = await browser.newPage();
		await page.setCookie({
			name: 'gift',
			value: flag,
			domain: 'web',
			httpOnly: true,
			secure: true,
			sameSite: 'None'
		});
		await page.goto(url,{ waitUntil: 'domcontentloaded', timeout: 3000 });
		await new Promise(r=>setTimeout(r,25000));
	}catch(e){ console.log(e) }
	try{await browser.close();}catch(e){}
	process.exit(0)
}

visit(JSON.parse(process.argv[2]))
