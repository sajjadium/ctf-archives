#!/usr/bin/env node
const express = require('express')
const rateLimit = require('express-rate-limit')
const bot = require('./bot')

const app = express()

app.get('/visit',rateLimit.rateLimit({
	windowMs: 60 * 1000,
	max: 1,
	message: 'o/',
	standardHeaders: 'draft-7', 
	legacyHeaders: false, 
}),(req,res)=>{
	if(req.query.url){
		bot.visit(req.query.url.toString())
	}
	res.send('Done')
})

app.listen(8002)
