#!/usr/bin/env node
const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const crypto = require('crypto');
const zlib = require('zlib');
const fs = require('fs');
const opsHandler = require('./ops');
const buffer = require('buffer');
const memoryStore = require('memorystore')
const rateLimit = require('express-rate-limit')

const flag = process.env['FLAG'] || 'WACON{test-flag}'
const adminSecret = process.env['ADMIN_SECRET'] || 'SECRET';
const noteTemplate = `<style>body {overflow-wrap: anywhere;font-family: sans-serif;color: white;font-size: 18px;}</style>`;
const flagTokens = new Map();
const notePaths = new Map();
const app = express();
const getHtmlPath = p=>`${__dirname}/html/${p}.html`;
const genToken = e=>crypto.randomBytes(e).toString('hex');
const toBuffer = e=>(Buffer.isBuffer(e) ? e : Buffer.from(e,'utf8'));
const now = _=>Math.trunc(Date.now()/1000);

app.use(cookieParser());
app.use(express.static('static', { maxAge: 1000*60*60 }));
app.use(express.urlencoded({ extended: false }));
app.use(session({
	resave: false,
	saveUninitialized: false,
	store: new (memoryStore(session))({
		checkPeriod: 86400000
	}),
	secret: genToken(16),
	cookie: { httpOnly: true, secure: false, sameSite: 'Lax' }
}));

app.get('/',(req,res)=>{
	res.sendFile(getHtmlPath('index'));
});

app.get('/view/:id/',(req,res)=>{
	res.sendFile(getHtmlPath('view'));
});

app.use((req,res,next)=>{
	res.setHeader('Content-Security-Policy',`default-src 'self'; style-src 'unsafe-inline'; `);
	res.setHeader('Cache-Control',`no-cache, no-store`);
	req.session.isAdmin ??= req.cookies.secret == adminSecret;
	req.session.uid ??= genToken(16);
	req.session.notes ??= [];

	next();
});

app.post('/',async (req,res)=>{
	try{
		let note = req.body.note;
		if(note){
			let userDir = `${__dirname}/notes/${req.session.uid}`;
			let noteId = genToken(16);
			let noteFilepath = `${userDir}/${noteId}.bin`;
			note = note.toString().trim().slice(0,1000);

			fs.existsSync(userDir) || fs.mkdirSync(userDir);

			fs.writeFileSync(noteFilepath,zlib.deflateSync(note));
			notePaths.set(noteId,noteFilepath);
			req.session.notes.push(noteId);
			return res.redirect(`/view/${noteId}/`);
		}
	}catch(e){}
	res.type('text/plain').send('Something went wrong');
});

app.put('/get_temp_token',(req,res)=>{
	if(req.session.isAdmin){
		let tok = genToken(4);
		flagTokens.set(tok,now());
		return res.type('text/plain').send(tok);
	}
	res.type('text/plain').send('??');
})

app.post('/flag',rateLimit.rateLimit({
	windowMs: 60 * 1000,
	max: 1,
	message: 'Too fast',
}),(req,res)=>{
	let tok = req.body.token;
	if(tok){
		if(flagTokens.get(tok)+60 > now()){
			return res.type('text/plain').send(`Whoaaa good job!!! : ${flag}`);
		}
	}
	res.type('text/plain').send('??');
})

app.get('/view/:noteid/render/*',(_,__,next)=>setTimeout(next,Math.random()*100),async (req,res)=>{
	try{
		let noteId = req.params.noteid.replaceAll(/[^a-f0-9]/g,'');
		let notePath = notePaths.get(noteId);
		let ops = req.path.split('/').slice(4).map(e=>
			(e && opsHandler.hasOwnProperty(e)) ? opsHandler[e] : e=>e
		);

		if(ops.length > 10) return res.type('text/plain').send('Error: Too many operations');

		if( notePath && 
			((req.session.notes.indexOf(noteId) > -1) || req.session.isAdmin) &&
			fs.existsSync(notePath)
			){
			let input = zlib.inflateSync(fs.readFileSync(notePath));
			ops.forEach(e=>(input = toBuffer(e(input))));
			input = buffer.isAscii(input) ? input : btoa(input);
			return res.send(noteTemplate+input);
		} else {
			return res.type('text/plain').send('Error: Not found');
		}
	} catch(e){console.log(e)}
	res.type('text/plain').send('Error: Something went wrong');
});

app.listen(8004);
