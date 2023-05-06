#!/usr/bin/env node
const express = require('express')
const childProcess = require('child_process')
const expressSession = require('express-session')
const fs = require('fs')
const crypto = require('crypto')
const app = express()
const flag = process.env.FLAG || process.exit()
const genRequestToken = () => Array(32).fill().map(()=>"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".charAt(Math.random()*62)).join("")

app.use(express.static("./static"))
app.use(expressSession({
	secret: crypto.randomBytes(32).toString("base64"),
	resave: false,
	saveUninitialized: true,
	cookie: { secure: false, sameSite: 'Lax' }
}))
app.use(express.json())

app.post('/request',(req,res)=>{
	const url = req.body.url
	const reqToken = genRequestToken()
	const reqFileName = `./request/${reqToken}`
	const outputFileName = `./output/${genRequestToken()}`

	fs.writeFileSync(reqFileName,[reqToken,req.session.id,"Processing..."].join('|'))
	setTimeout(()=>{
		try{
			const output = childProcess.execFileSync("timeout",["2","jp2a",...url])
			fs.writeFileSync(outputFileName,output.toString())
			fs.writeFileSync(reqFileName,[reqToken,req.session.id,outputFileName].join('|'))
		} catch(e){
			fs.writeFileSync(reqFileName,[reqToken,req.session.id,"Something bad happened!"].join('|'))
		}
	},2000)
	res.redirect(`/request/${reqToken}`)
})

app.get("/request/:reqtoken",(req,res)=>{
	const reqToken = req.params.reqtoken
	const reqFilename = `./request/${reqToken}`
	var content
	if(!/^[a-zA-Z0-9]{32}$/.test(reqToken) || !fs.existsSync(reqFilename)) return res.json( { failed: true, result: "bad request token." })

	const [origReqToken,ownerSessid,result] = fs.readFileSync(reqFilename).toString().split("|")

	if(req.session.id != ownerSessid) return res.json( { failed: true, result: "Permissions..." })
	if(result[0] != ".") return res.json( { failed: true, result: result })

	try{
		content = fs.readFileSync(result).toString();
	} catch(e) {
		return res.json({ failed: false, result: "Something bad happened!" })
	}

	res.json({ failed: false, result: content })
	res.end()
})

app.get("/flag",(req,res)=>{
	if(req.ip == "127.0.0.1" || req.ip == "::ffff:127.0.0.1") res.json({ failed: false, result: flag })
	else res.json({ failed: true, result: "Flag is not yours..." })
})

function clearOutput(){
	try{
		childProcess.execSync("rm ./output/* ./request/* 2> /dev/null")
	} catch(e){}
	setTimeout(clearOutput,120e3)
}

clearOutput()
app.listen(9000)
