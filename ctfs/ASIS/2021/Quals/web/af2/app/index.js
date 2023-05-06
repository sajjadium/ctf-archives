#!/usr/bin/env node
const express = require("express")
const cookieParser = require('cookie-parser')
const puppeteer = require("puppeteer")
const app = express()
const adminPassword = process.env.ADMINPASSWD || 'admin'
const flag = process.env.FLAG || "flag{fake-flag}"
const authTokens = new Map()
const passCodes = new Map()
const flagIpsList = new Map()
const reportIpsList = new Map()
const passcodeHTML = require("fs").readFileSync("./public/passcode.html").toString()

const genSessToken = () => Array(32).fill().map(()=>"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".charAt(Math.random()*62)).join("")
const genPasscode = () => Array(16).fill().map(()=>"01234567".charAt(Math.random()*8)).join("")
const now = ()=>Math.floor(+new Date()/1000)

app.use(cookieParser())
app.use(express.urlencoded({ extended: true }))
app.use((req,res,next)=>{
	res.setHeader("Cache-Control","no-cache,no-store")
	next()
})
app.use(express.static('public'))

app.get("/report",(req,res)=>{
	res.sendFile("./report.html",{ root:"./public" })
})

app.post("/report",async (req,res)=>{
	res.setHeader("Content-Type","text/plain")
	if(typeof req.body.url != "string" || !/^https?:\/\//.test(req.body.url)) return res.send("Bad url!")

	if(reportIpsList.has(req.ip) && reportIpsList.get(req.ip)+30 > now()){
		return res.send(`Please comeback ${reportIpsList.get(req.ip)+30-now()}s later!`)
	}
	reportIpsList.set(req.ip,now())

	const browser = await puppeteer.launch({pipe:true,executablePath: '/usr/bin/google-chrome'})
	var page = await browser.newPage()
	await page.goto("http://localhost:9000")
	await page.waitForSelector('#username')
	await page.type('#username', 'admin')
	await page.type('#password', adminPassword)
	await page.click("#submit")
	await page.waitForSelector("#backlink")
	await page.close()

	page = await browser.newPage()
	res.send("Admin is visiting your URL")
	try{
		await page.goto(req.body.url,{
			timeout: 2000
		})
		// Author's note: The intended solution works under 30 secs, the attacker's server ( actually it's my home network ) ping to the instance is 130ms. If the server you are using is not close to our instace, you can use free web hostings. 
		await new Promise(resolve => setTimeout(resolve, 40e3));
	} catch(e){}
	await page.close()
	await browser.close()
})

app.post("/signin",(req,res)=>{
	if(req.body.username == "admin" && req.body.password == adminPassword){
		const authToken = genSessToken()
		const passCode = genPasscode()

		passCodes.set(passCode,now()+60)
		authTokens.set(authToken,passCode)

		res.cookie('auth_token', authToken, { sameSite: "Lax", httpOnly: true })
		res.sendFile("./login_success.html",{ root: "./public" })
	} else {
		res.sendFile("./login_failed.html",{ root: "./public" })
	}
})

app.get("/",(req,res)=>{
	res.setHeader("X-Frame-Options","SAMEORIGIN")
	res.setHeader("Content-Security-Policy","script-src 'none'; img-src 'none'; frame-src 'self'; font-src data: ;")
	res.setHeader("Cache-Control","no-store,no-cache")

	const userAuthToken = req.cookies.auth_token
	if(typeof userAuthToken == "string" && authTokens.has(userAuthToken)){
		const passCode = authTokens.get(userAuthToken)
		authTokens.delete(userAuthToken)
		if(passCodes.has(passCode)){
			return res.send(passcodeHTML.replace("$PASSCODE$",passCode).replace("$NOTE$",req.query.note ? req.query.note : "Have fun!"))
		}
	}
	res.sendFile("./home.html",{root:"./public"})
})

app.get("/flag",(req,res)=>{
	const passCode = typeof req.query.passcode == "string" && /^[0-9]{16}$/.test(req.query.passcode) ? req.query.passcode : "_"
	res.setHeader("Content-Type","text/plain")
	if(flagIpsList.has(req.ip) && flagIpsList.get(req.ip)+30 > now()){
		return res.send(`Please comeback ${flagIpsList.get(req.ip)+30-now()}s later!`)
	}
	flagIpsList.set(req.ip,now())
	if(passCodes.has(passCode)){
		if(passCodes.get(passCode) > now()){
			res.send(flag)
		} else {
			res.send("Expired")
		}
		passCodes.delete(passCode)
	} else {
		res.send("??")
	}
})

app.listen(9000)