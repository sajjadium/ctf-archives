#!/usr/bin/env node
const express = require('express')
const ejs = require('ejs')
const bodyParser = require('body-parser')

const app = express()
const exampleTemplate = `
Hi ~nameOfHacker~,

We wish you a lot of flags and vulns in the new year!

~flag~

Cheers, 
~nameOfSender~
`
app.use(bodyParser.text());

app.use((req,res,next)=>{
	/*
		Avoiding possible crashes.
		This part isn't really part of the challenge.
	*/
	req.socket.on('error',()=>{})
	req.on('error',()=>{})
	next()
})

app.get('/',(req,res)=>res.send('hi'))

app.post('/internal/gen_email_template',(req,res)=>{
	let template = req.body

	if(typeof req.body != 'string'){
		template = exampleTemplate
		req.query = {
			'nameOfHacker': 'player',
			'nameOfSender': 'asis'
		}
	}

	req.query.flag = process.env.FLAG

	let varsList = Array.from(template.matchAll(/(~.*?~)/g))
	varsList.forEach((item)=>{
		let varName = item[1].slice(1,-1)
        if(typeof req.query[varName] == 'string'){
            template = template.replace(item[1],req.query[varName])
        }
	})
	template = template.slice(0,1024*1024)

	return res.send(template)
})

app.listen(80)