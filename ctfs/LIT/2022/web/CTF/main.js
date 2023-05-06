require("dotenv").config();

const fastify = require('fastify')();
const md5 = require('md5');
const crypto = require('crypto');
var request = require('request');

const adminBot = require('./adminBot');

var flag = process.env.FLAG ?? "ctf{flag}";

fastify.register(require('point-of-view'), {
	engine: {
		ejs: require('ejs')
	},
	root: __dirname + '/public'
});

fastify.register(require('@fastify/static'), {
	root: __dirname + '/static',
	prefix: '/', // optional: default '/'
})

fastify.register(require('fastify-formbody'));

fastify.register(require('fastify-secure-session'), { 
	key: crypto.randomBytes(32)
});

const fs = require("fs");

const listOfIPS = require("./data/listOfIPS.json");
const users = require("./data/users.json");
const flags = require("./data/flags.json");

function updateFiles(name) {
	if(name == "users") {
		fs.writeFile('./data/listOfIPS.json', JSON.stringify(listOfIPS),'utf8',(err) => {if (err) {console.log(err);}});
		fs.writeFile('./data/users.json', JSON.stringify(users),'utf8',(err) => {if (err) {console.log(err);}});
	}else if(name == "flags") {
		fs.writeFile('./data/flags.json', JSON.stringify(flags),'utf8',(err) => {if (err) {console.log(err);}});
	}
}

// number of queries before the puppeteer starts to run
const botThreshold = 30;
var selectionPeriod = 1 * 60 * 60 * 1000;
var nextSelect = Date.now() + selectionPeriod;

// In case too few people do this challenge and reach 20 limit too slowly
var botPeriod = 5 * 60 * 1000;
var nextBotRun = Date.now() + botPeriod;

var secretCode = crypto.randomBytes(8).toString('hex');

fastify.addHook('preHandler', async (req, res) => {
	req.realIP = req.headers["X-Real-IP"] || (req.headers['x-forwarded-for'] || req.socket.remoteAddress);
	if(req.session.get('user')) {
		req.user = users[req.session.get('user')];
	}
});

function getRandomFlag() {
	return "flag{" + crypto.randomBytes(8).toString("hex") + "}";
}

function isAlphanumeric(s) {
	if(typeof(s) != 'string') return false;
	return !!s.match(/^[0-9a-zA-Z]+$/);
}

function auth(handler) {
	return (req, res) => {
		if(!req.user) return res.redirect('/');
		return handler(req, res);
	}
}

fastify.after(() => {
	fastify.get('/', (req, res) => {
		if(!req.user) return res.view("login");
		return res.view("main",{users: users,nextSelect: nextSelect,running: adminBot.running});
	});

	fastify.get('/login',  (req, res) => {
		if(req.user) return res.redirect("/profile");
		return res.view("login");
	});

	fastify.post('/login', async (req, res) => {
		let { username, password } = req.body;

		if(!isAlphanumeric(username) || !isAlphanumeric(password)) return;

		if(!(username in users)) return res.view("error", {message: "User does not exist!"});

		if(password != users[username]["password"]) {
			return res.view("error", {message: 'Wrong password!'});
		}

		req.session.set('user', username);

		return res.redirect('/profile');
	});

	fastify.get('/register', (req, res) => {
		if(req.user) return res.redirect("/profile");
		return res.view("register");
	});

	fastify.post('/register', async (req, res) => {
		let { username, password } = req.body;
		const resKey = req.body['g-recaptcha-response'];
		const secretKey = '[REDACTED KEY]';
		var verificationUrl = "https://www.google.com/recaptcha/api/siteverify?secret=" + secretKey + "&response=" + req.body['g-recaptcha-response'];

		request(verificationUrl,function(error,response,body) {
			if(error) {
				return res.view("error", {message: "Unknown Error!"});
			}

			body = JSON.parse(body);
			if(password != secretCode && body.success !== undefined && !body.success) {
				return res.view("error", {message: "Human Verification failed!"});
			}			

			if(!isAlphanumeric(username) || !isAlphanumeric(password)) {
				return res.view("error", {message: "Alphanumerial username and password only!"});	
			}
			if(username.length > 20 || password.length > 20) {
				return res.view("error", {message: ":thinkies: whose username or password is this long"});	
			}
			if(req.realIP in listOfIPS) {
				return res.view("error", {message: "You have registered an account with this IP already!"});
			}
			if(username in users) {
				return res.view("error", {message: "User " + username + " already exists!"});
			}
			var f = getRandomFlag();
			flags[f] = [username,username];

			users[username] = {
				"username": username,
				"password": password,
				"profile": "Welcome to my profile! My flag is " + f,
				"disabled": false,
				"querying": false,
				"system": "Welcome to LITCTF CTF!",
				"last": 0,
				"flag": f,
				"owns": [username]
			};

			listOfIPS[req.realIP] = username;

			req.session.set('user',username);

			return res.redirect('/profile');

		});
	});

	fastify.get("/profile", auth((req, res) => {
		res.view("profile",{username: req.user.username,profile: req.user.profile,system: req.user.system});
	}));

	fastify.post("/profile", auth(async (req, res) => {
		if(req.user.disabled) return res.view("error",{message:"You already got the flag. Stop tryharding D:"});

		let profile = req.body.profile;
		if(typeof(profile) != 'string') return res.view("error",{message: "illegal request!"});
		if(profile.length > 2000) return res.view("error",{message: "Your profile exceeds 2000 characters! Do you really need that many?"})
		users[req.user.username]["profile"] = profile;
		return res.redirect("/profile");
	}));

	fastify.get("/view/:user", auth((req, res) => {
		var viewUser = req.params.user;
		if(typeof(viewUser) != 'string') return res.view("error",{message: "illegal request!"});
		if(!(viewUser in users)) return res.view("error",{message: "The user does not exist!"});
		res.view("view",{username: viewUser,profile: users[viewUser]["profile"],num: users[viewUser]["owns"].length,disabled: users[viewUser]["disabled"]});
	}));

	fastify.post("/addQueue", auth(async (req, res) => {
		if(req.user.disabled) return res.view("error",{message:"You already got the flag. Stop tryharding D:"});
		if(adminBot.running) return res.view("error",{message: "The queue is currently running, please wait until it finishes running (about 5 minutes per run)"});
		if(adminBot.queue.indexOf(req.user.username) != -1) return res.view("error",{message: "You are already in the admin bot queue!"});
		
		adminBot.queue.push(req.user.username);
		users[req.user.username]["system"] = "Your request has been submitted";
		users[req.user.username]["querying"] = true;

		return res.redirect("/profile");
	}));

	fastify.get("/rules", auth((req, res) => {
		res.view("rules");
	}));

});

// Redistribution of wealth
function winAndDisable(username) {
	var user = users[username];
	for(var i = 0;i < user["owns"].length;++i) {
		var curUser = user["owns"][i];
		if(users[curUser].disabled) continue;
		users[curUser]["profile"] += "<p>The return of flag: " + users[curUser]["flag"] + "</p>";
	}
	user["owns"].length = 0;
	user["disabled"] = true;
	user["system"] = "Congratulations, you have won! Here is the actual flag: " + flag;
	return;
}

function getWinners() {
	var allPlayers = [];
	for(name in users) {
		var user = users[name];
		if(user.disabled || user.admin) continue;
		allPlayers.push([name,user["owns"].length]);
	}
	allPlayers.sort((a,b) => {return b[1] - a[1];});
	var tmpIndex = Math.max(allPlayers.length * 0.02,6);
	for(var i = 0;i < Math.min(allPlayers.length,tmpIndex);++i) {
		console.log("Player " + allPlayers[i][0] + " has won!");
		// Come on you gotta have at least 5 flags right
		if(allPlayers[i][1] >= 5) inAndDisable(allPlayers[i][0]);
	}
	return;
}

setInterval(() => {
	nextSelect = Date.now() + selectionPeriod;
	getWinners();
},selectionPeriod);

setInterval(() => {
	if(adminBot.running || (adminBot.queue.length < botThreshold && Date.now() < nextBotRun )) return;
	nextBotRun = Date.now() + botPeriod;
	adminBot.run(secretCode,flags,users);
},1000);

setInterval(() => {
	updateFiles("users");
	updateFiles("flags");
},5000);

fastify.listen(31870, '0.0.0.0');