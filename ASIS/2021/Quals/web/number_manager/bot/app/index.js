#!/usr/bin/node
const puppeteer = require("puppeteer");
const fs = require("fs");
const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
});
const getDate = ()=>Math.floor(+new Date/1000);
const remoteIP = process.env.REMOTE_HOST;
var blacklist = {};

async function crawl(url){
	const browser = await puppeteer.launch({pipe:true,executablePath: '/usr/bin/google-chrome'});
	const page = await browser.newPage();
	try{
		await page.goto("http://nmanager",{
			timeout: 2000
		});
		await page.waitForSelector('#num');
		await page.type('#num', '373638');
		await page.type('#desc', 'what is this??');
		await page.click('#addbtn');
		await page.goto("about:blank",{
	  		timeout: 2000
		});
		await page.goto(url,{
	  		timeout: 2000
		});
		process.stdout.write(`Navigated to ${url}.\n`);
		await new Promise(resolve => setTimeout(resolve, 5e3));
	} catch(e){}
	process.stdout.write(`Closing browser.\n`);
	await page.close();
	await browser.close();
	process.exit();
}

try {
	blacklist = JSON.parse(fs.readFileSync("/tmp/blacklist.json"));
} catch(e){}

if( getDate() < blacklist[remoteIP]+30){
	process.stdout.write(`Please comeback ${blacklist[remoteIP]+30-getDate()}s later\n`);
	process.exit();
}
blacklist[remoteIP] = getDate();
fs.writeFileSync("/tmp/blacklist.json",JSON.stringify(blacklist))

readline.question('URL: ', url => {
	if(/^https?:\/\//.test(url)) crawl(url);
	else readline.close() && process.exit();
});
