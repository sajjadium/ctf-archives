#!/usr/bin/env node
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const request = require('request')
const puppeteer = require('puppeteer')

const app = express()
const cSiteKey = process.env.SITE_KEY || ''
const cPrivateKey = process.env.SECRET_KEY || ''
const secretToken = process.env.SECRET_TOKEN || 'lol'
const challDomain = process.env.CHALL_DOMAIN || 'localhost'

const flag = process.env.FLAG || 'ASIS{test-flag}'
const indexHtml = require('fs').readFileSync('./index.html').toString().replace('$SITEKEY$',cSiteKey)
const reportIpsList = new Map()
const now = ()=>Math.floor(+new Date()/1000)

app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

app.get('/',(req,res)=>{
	var msg = req.query.msg
	if(!msg) msg = `Yo you want the flag? solve the captcha and click submit.\\nbtw you can't have the flag if you don't have the secret cookie!`
	msg = msg.toString().toLowerCase().replace(/\'/g,'\\\'').replace('/script','\\/script')
	res.send(indexHtml.replace('$MSG$',msg))
})

app.post('/flag',(req,res)=>{
	const resp = req.body['g-recaptcha-response']
	res.type('txt')
	if(!resp || req.cookies.secret_token != secretToken) return res.send('??')
	const u = "https://www.google.com/recaptcha/api/siteverify?secret=" + cPrivateKey + "&response=" + resp
	request(u,function(error,response,body) {
		if(error) return res.send('Error :(')
		body = JSON.parse(body);

		if(!body.success) {
			return res.send('Error :(');
		} else {
			return res.send(flag)
		}
	});
})

app.get('/report',(req,res)=>{
	res.sendFile('./report.html',{ root: '.' })
})

app.post("/report",async (req,res)=>{
	res.setHeader("Content-Type","text/plain")
	if(typeof req.body.url != "string" || !/^https?:\/\//.test(req.body.url)) return res.send("Bad url!")

	if(reportIpsList.has(req.ip) && reportIpsList.get(req.ip)+30 > now()){
		return res.send(`Please comeback ${reportIpsList.get(req.ip)+30-now()}s later!`)
	}
	reportIpsList.set(req.ip,now())

	const browser = await puppeteer.launch({ pipe: true,executablePath: '/usr/bin/google-chrome' })
	const page = await browser.newPage()
	await page.setCookie({
		name: 'secret_token',
		value: secretToken,
		domain: challDomain,
		httpOnly: true,
		secret: false,
		sameSite: 'Lax'
	})

	res.send("Bot is visiting your URL")
	try{
		await page.goto(req.body.url,{
			timeout: 2000
		})
		await new Promise(resolve => setTimeout(resolve, 5e3));
	} catch(e){}
	await page.close()
	await browser.close()
})

app.listen(8000)