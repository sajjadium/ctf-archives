const cookieParser = require('cookie-parser');
const express = require('express');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

const flag = "[redacted]";

let secrets = [];

const app = express()
app.use('/style.css', express.static('style.css'));
app.use('/favicon.ico', express.static('favicon.ico'));
app.use('/rick.png', express.static('rick.png'));
app.use(cookieParser())

app.use('/admin',(req, res, next)=>{
	res.locals.rolled = true;
	next();
})

app.use((req, res, next) => {
	let cookie = req.cookies?req.cookies.session:"";
	res.locals.flag = false;
	try {
		let sid = JSON.parse(Buffer.from(cookie.split(".")[1], 'base64').toString()).secretid;
		if(sid==undefined||sid>=secrets.length||sid<0){throw "invalid sid"}
		let decoded = jwt.verify(cookie, secrets[sid]);
		if(decoded.perms=="admin"){
			res.locals.flag = true;
		}
		if(decoded.rolled=="yes"){
			res.locals.rolled = true;
		}
		if(res.locals.rolled) {
			req.cookies.session = ""; // generate new cookie
		}
	} catch (err) {
		req.cookies.session = "";
	}
	if(!req.cookies.session){
		let secret = crypto.randomBytes(32)
		cookie = jwt.sign({perms:"user",secretid:secrets.length,rolled:res.locals.rolled?"yes":"no"}, secret, {algorithm: "HS256"});
		secrets.push(secret);
		res.cookie('session',cookie,{maxAge:1000*60*10, httpOnly: true})
		req.cookies.session=cookie
		res.locals.flag = false;
	}
	next()
})

app.get('/admin', (req, res) => {
	res.send("<!DOCTYPE html><head></head><body><script>setTimeout(function(){location.href='//goo.gl/zPOD'},10)</script></body>");
})

app.get('/', (req, res) => {
	res.send("<!DOCTYPE html><head><link href='style.css' rel='stylesheet' type='text/css'></head><body><h1>hello kind user!</h1><p>your flag is <span style='color:red'>"+(res.locals.flag?flag:"error: insufficient permissions! talk to the <a href='/admin'"+(res.locals.rolled?" class='rolled'":"")+">admin</a> if you want access to the flag")+"</span>.</p><footer><small>This site was made extra secure with signed cookies, with a different randomized secret for every cookie!</small></footer></body>")
})

app.listen(3000)