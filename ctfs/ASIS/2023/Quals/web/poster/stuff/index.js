#!/usr/bin/env node
const express = require('express');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const childProcess = require('child_process');

const app = express();
const badCTypes = ['plain','form','csp'];
const genToken = e=>crypto.randomBytes(16).toString('hex');
const sessions = new Map();
const captchaSecret = process.env.CAPTCHA_SECRET || ''

app.use(cookieParser());
app.use(express.static('./static'));
app.use((req,res,next)=>{
	if(!sessions.get(req.cookies.session)){
		let newSession = genToken();
		sessions.set(newSession,{
			csrfToken: genToken(),
			secret: '',
		});
		res.cookie('session', newSession, {
			secure: true,
			sameSite: 'None',
			httpOnly: true
		});
		req.session = sessions.get(newSession);
	} else {
		req.session = sessions.get(req.cookies.session);
	}
	next();
})
app.use((req, res, next)=>{
	if(req.method == 'POST'){
		req.body = '';
		req.on('data', (c)=>req.body+=c);
		req.on('end',_=>{
			const ctype = req.get('Content-Type')+'';
			req.body = new URLSearchParams(req.body);
			req.isCsrf = badCTypes.some(e=>(ctype.indexOf(e) != -1));
			req.isCsrf |= !(req.session.csrfToken && req.body.get('csrf_token'));
			req.isCsrf |= req.session.csrfToken != req.body.get('csrf_token');
			next();
		});
	} else {
		next();
	}
});

app.post('/secret',(req,res)=>{
	if(!req.isCsrf){
		req.session.secret = req.body.get('secret');
		res.json(true);
	} else {
		res.json(false);
	}
})
app.get('/secret',(req,res)=>res.json(req.session.secret));
app.get('/csrf-token',(req,res)=>res.json(req.session.csrfToken));
app.post('/report',(req,res)=>{
	let gresp = req.body.get('g-recaptcha-response')?.toString();
	let url = req.body.get('url')?.toString();

	res.type('text/plain')
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
