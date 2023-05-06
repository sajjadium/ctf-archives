#!/usr/bin/env node
const express = require("express");
const puppeteer = require("puppeteer");
const fs = require("fs");
const indexHtml = fs.readFileSync("./index.html").toString();
const app = express();
const ipsList = new Map();

const genNonce = ()=>"_".repeat(16).replace(/_/g,()=>"abcdefghijklmnopqrstuvwxyz0123456789".charAt(Math.random()*36));
const now = ()=>Math.floor(Date.now() / 1000);

app.use('/static', express.static('static'))

app.get('/', function(req, res){
	res.setHeader("Content-Type","text/html");
	res.send(indexHtml.replace(/\$NONCE\$/g,genNonce()));
});

app.get('/report', async function(req, res){
	const url = req.query.url;
	if(!/^https?:\/\//.test(url)){
		return res.send("i don't like this url!");
	}

	if(ipsList.has(req.ip) && ipsList.get(req.ip)+30 > now()){
		return res.send(`Please comeback ${ipsList.get(req.ip)+30-now()}s later!`);
	}
	ipsList.set(req.ip,now());

	const browser = await puppeteer.launch({pipe:true,executablePath: '/usr/bin/google-chrome'});
	const page = await browser.newPage();
	try{
		await page.setCookie({
			name: 'flag',
			value: process.env.FLAG || "flag{fake-flag}",
			domain: "localhost",
			expires: now() + 1000,
		});
		await page.goto(url,{
	  		timeout: 2000
		});
		await new Promise(resolve => setTimeout(resolve, 10e3));
	} catch(e){}
	await page.close();
	await browser.close();

	res.send("OK");
});

app.listen(8000);