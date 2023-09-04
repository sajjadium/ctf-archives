#!/usr/bin/env node
const express = require('express')
const rateLimit = require('express-rate-limit')
const fetch = require("isomorphic-fetch")
const bot = require('./bot')

const app = express()
app.use(express.urlencoded({ extended: false }));

app.get('/',(req,res)=>{
	res.send(`
<html>
	<head>
		<script src="https://www.google.com/recaptcha/api.js" async defer></script>
	</head>
	<body>
		<form action="/" method="POST">
		    <input type="text" name="url" placeholder="URL" required>
		    <br>
		    <div class="g-recaptcha"
		         data-sitekey="6LdNm_AnAAAAAJkZhaB3pDtpuCSlQZRCXVq4cAha">
		    </div>
		    <br>
		    <button type="submit">Submit</button>
		</form>
	</body>
</html>
	`)
})

app.post('/',rateLimit.rateLimit({
	windowMs: 40 * 1000,
	max: 1,
	message: 'Only one try every 40 seconds',
	standardHeaders: 'draft-7', 
	legacyHeaders: false, 
}),(req,res)=>{
	let url = req.body.url
	let response_key = req.body["g-recaptcha-response"];
	let secretKey = '__________________________________'


	if(!response_key || !url || (!url.startsWith('http://') && !url.startsWith('https://'))){
		res.type('text/plain').send('bad url')
		return;
	}

	fetch(`https://www.google.com/recaptcha/api/siteverify?secret=${secretKey}&response=${encodeURIComponent(response_key)}`, {
	    method: "POST"
	}).then((response)=>response.json()).then(r=>{
		if (r.success == true) {
			bot.visit(url.toString())
			return res.type('text/plain').send('Told the admin to visit your page!')
		} else {
			return res.type('text/plain').send('bad captcha?')
		}
	}).catch(e=>{
		return res.type('text/plain').send('bad captcha?')
	})
})

app.listen(8002)
