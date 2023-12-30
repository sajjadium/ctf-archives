#!/usr/bin/env node
const express = require('express')
const cookieParser = require('cookie-parser')

const app = express()

app.use(cookieParser())
app.use((req,res,next)=>{
	res.header(
		'Content-Security-Policy',
		[`default-src 'none';`, ...[(req.headers['sec-required-csp'] ?? '').replaceAll('script-src','')]] 
	)
	if(req.headers['referer']) return res.type('text/plain').send('You have a typo in your http request')
	next()
})

app.get('/',(req,res)=>{
	let gift = req.cookies.gift ?? 'ASIS{test-flag}'
	let letter = (req.query.letter ?? `You were a good kid in 2023 so here's a gift for ya: $gift$`).toString()
	res.send(`<pre>${letter.replace('$gift$',gift)}</pre>`)
})

app.listen(8000)
