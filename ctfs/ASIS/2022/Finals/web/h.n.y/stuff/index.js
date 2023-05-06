#!/usr/bin/env node
const express = require('express')
const crypto = require('crypto')
const { visit } = require('./bot')

const app = express()
const reportIpsList = new Map()
const indexTemplate = require('fs').readFileSync('./index.html').toString()
const now = ()=>Math.floor(+new Date()/1000)

app.use((req,res,next)=>{
	res.locals.nonce = crypto.randomBytes(16).toString("hex")
	res.setHeader('Content-Security-Policy',`default-src 'self'; script-src 'unsafe-eval' 'nonce-${res.locals.nonce}' `)
	res.setHeader('X-Frame-Options','DENY')
	next()
})

app.get('/',(req,res)=>{
	let s = indexTemplate.replace('$nonce$',()=>res.locals.nonce)
	s = s.replace('MSG',()=>(req.query.p ?? '<code>( ˘▽˘)っ♨</code>').slice(0,0x1000))
	res.send(s)
})

app.get('/hack',(req,res)=>{
	if(reportIpsList.has(req.ip) && reportIpsList.get(req.ip)+60 > now()){
		return res.send(`Please comeback ${reportIpsList.get(req.ip)+60-now()}s later!`)
	}
	reportIpsList.set(req.ip,now())
	
	visit(req.query.p.toString())
	res.send('ok')
})

app.listen(9000,_=>{
	console.log('[+] Listening on 9000')
})
