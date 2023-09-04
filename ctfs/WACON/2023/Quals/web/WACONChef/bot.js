#!/usr/bin/env node
const puppeteer = require('puppeteer');

const challUrl = process.env['CHALL_URL'] ||'http://vm:8000';
const challDomain = process.env['CHALL_DOMAIN'] ||'vm';
const secretToken = process.env['ADMIN_SECRET'] || 'SECRET';

exports.visit = async function (url){
	let browser;

	if(!url.startsWith('http://') && !url.startsWith('https://')){
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
		await page.setCookie({
			httpOnly: true,
			name: 'secret',
			value: secretToken,
			domain: challDomain,
			sameSite: 'Lax'
		});
		await page.goto(challUrl);
		await page.waitForSelector('textarea');
		console.log(await page.evaluate(async ()=>{
			let token = await fetch('/get_temp_token',{method:'PUT'});
			token = await token.text();
			document.querySelector("textarea").value = token;
			document.querySelector("button").click();
			return token
		}));
		await page.waitForSelector('#todo-select');
		let targetUrl = await page.evaluate(() => document.location.href);
		await page.close();

		page = await browser.newPage();
		await page.goto(url+'target='+encodeURIComponent(targetUrl), {timeout: 2000, waitUntil: 'domcontentloaded'})
		if(url.indexOf('i_want_flags') > -1){
			await new Promise((r)=>setTimeout(r,40000))	;
		} else {
			await new Promise((r)=>setTimeout(r,5000));
		}
		
	}catch(e){
		console.log(e);
	}
	try{await browser.close()}catch(e){}
}

