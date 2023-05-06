#!/usr/bin/env node
const puppeteer = require('puppeteer')

const flag = process.env.FLAG ?? 'flag{test-flag}'

async function visit(url){
	let browser

	if(!/^https?:\/\//.test(url)){
		return;
	}

	try {		
		browser = await puppeteer.launch({
		    pipe: true,
		    args: [
		        "--no-sandbox",
		        "--disable-setuid-sandbox",
		        "--js-flags=--noexpose_wasm,--jitless",
		    ],
		    executablePath: "/usr/bin/google-chrome",
		})

		let page = await browser.newPage()
		await page.setCookie({name: 'flag', value: flag, domain: 'localhost'})
		await page.goto(url, { timeout: 1000, waitUntil: 'domcontentloaded' })
		await new Promise((r)=>setTimeout(r,3000))
		await page.close()
		await browser.close()
		browser = null
    } catch(err){
    	console.log(err)
    } finally {
        if (browser) await browser.close()
    }
}
exports.visit = visit
