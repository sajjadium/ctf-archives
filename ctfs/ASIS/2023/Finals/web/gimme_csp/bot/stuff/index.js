#!/usr/bin/env node
const express = require('express')
const childProcess = require('child_process');

const app = express();
const captchaSecret = process.env.CAPTCHA_SECRET || '';

app.use(express.static('./static'));
app.use(express.urlencoded({ extended: false }));

app.post('/report',(req,res)=>{
	let gresp = req.body['g-recaptcha-response']?.toString();
	let url = req.body.url?.toString();

	res.type('text/plain');
	if(gresp && url && (url.startsWith('http://') || url.startsWith('https://'))){
		fetch(`https://www.google.com/recaptcha/api/siteverify?secret=${captchaSecret}&response=${encodeURIComponent(gresp)}`, {
	        method: 'POST'
	    }).then(response => response.json()).then(r => {
	    	if(r.success == true){
				childProcess.spawn('node',['./bot.js',JSON.stringify(url)]);
    			res.send('Admin will visit!');
	    	} else {
				res.send('Captcha failed i guess');
	    	}
	    }).catch(error => res.send('Unknown error??'));
	} else {
		res.send('Bad params');
	}
});

app.listen(8000);

