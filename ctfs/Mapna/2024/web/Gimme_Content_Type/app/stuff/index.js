#!/usr/bin/env node
const express = require('express')
const cookieParser = require('cookie-parser')
const prevGifts = new Set()

const app = express()

app.use(cookieParser())
app.use((req,res,next)=>{
	res.header('Content-Security-Policy',`default-src 'none';`)
	res.header('Cache-Control','no-store, no-cache')
	if(req.headers['sec-fetch-mode'] == 'navigate'){
		let userGift = req.cookies.gift
		if(!prevGifts.has(userGift)){
			prevGifts.add(userGift)
			req.gift = userGift 
		}
	}
	next()
})

app.get('/',(req,res)=>{
	let ct = req.query.content_type ?? 'text/plain'
	if(/^[a-z]+\/[a-z]+$/.test(ct)){
		res.setHeader('Content-Type', ct)
	}
	let letter = (req.query.letter ?? `$gift$`).toString().replaceAll('\x00','')
	letter = letter.replace('$gift$',`Here's your gift: "${req.gift ?? "MAPNA{1337}"}"`)
	res.send(letter)
})

app.listen(8000)
