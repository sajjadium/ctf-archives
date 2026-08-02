// Credit: I copied a lot of code from EhhThing's challenge Noted from PicoCTF 2022
// However note that the actual exploits are completely unrelated

global.Buffer = global.Buffer || require('buffer').Buffer;

if (typeof btoa === 'undefined') {
  global.btoa = function (str) {
    return new Buffer(str, 'binary').toString('base64');
  };
}

if (typeof atob === 'undefined') {
  global.atob = function (b64Encoded) {
    return new Buffer(b64Encoded, 'base64').toString('binary');
  };
}

require("dotenv").config();

const fastify = require('fastify')();
const md5 = require('md5');
const request = require("request");

const addFriend = require('./addFriend');

fastify.register(require('point-of-view'), {
	engine: {
		ejs: require('ejs')
	},
	root: __dirname + '/public'
});

fastify.register(require('fastify-formbody'));

fastify.register(require('fastify-secure-session'), { 
	key: require('crypto').randomBytes(32)
});

fastify.register(require('fastify-csrf'), {
	sessionPlugin: 'fastify-secure-session'
});

var users = Object.create(null);

fastify.addHook('preHandler', async (req, res) => {
	if(req.session.get('user')) {
		req.user = users[req.session.get('user')];
	}
});

function auth(handler) {
	return (req, res) => {
		if(!req.user) return res.redirect('/');

		return handler(req, res);
	}
}

fastify.after(() => {
	fastify.get('/', (req, res) => {
		if(req.user) return res.redirect('/view');
		return res.view("login");
	});

	fastify.post('/login', async (req, res) => {
		let { username, password } = req.body;

		if(!(username in users)) return res.view("error", {message: "User does not exist!"});

		if(password != users[username]["password"]) {
			return res.view("error", {message: 'Wrong password!'});
		}

		req.session.set('user', username);

		return res.redirect('/view');
	});

	fastify.get('/register', (req, res) => {
		return res.view("register");
	});

	fastify.post('/register', async (req, res) => {
		let { username, password, nickname, decade } = req.body;

		if(username in users) {
			return res.view("error", {message: "User " + username + " already exists!"});
		}

		if(md5(nickname) == "1f4e0a21bb6eef87c17ca2abdfc28369") {
			return res.view("error", {message: "I know what'you're doing. So you better think again >:D"});
		}

		users[username] = {
			"username": username,
			"password": password,
			"nickname": nickname,
			"decade": decade,
			"images": {}
		}

		req.session.set('user',username);

		return res.redirect('/view');
	});

	fastify.get('/view', auth(async (req, res) => {
		return res.view('view', {
			user: btoa(JSON.stringify(req.user))
		});
	}));

	fastify.get('/new', auth(async (req, res) => {
		return res.view('new', { csrf: await res.generateCsrf() });	
	}));

	fastify.post('/new', {
		preHandler: fastify.csrfProtection
	}, auth(async (req, res) => {
		let { url, description } = req.body;

		if(!users[req.user.username]["images"][req.user.nickname]) {
			users[req.user.username]["images"][req.user.nickname] = {};
		}
		users[req.user.username]["images"][req.user.nickname][md5(url).slice(0,6)] = [
			url,
			description,
		];

		return res.redirect('/view');
	}));

	fastify.get('/combineform', auth(async (req, res) => {
		return res.view('combineform', {});	
	}));

	fastify.get('/combine', auth(async (req, res) => {
		let { friendname, friendpassword } = req.query;
		if(!(friendname in users)) {
			return res.view("error", {message: "Friend does not exist!"});
		}
		if(users[friendname]["password"] != friendpassword) {
			return res.view("error", {message: "Friend password is wrong!"});			
		}
		return res.view('combine', {
			nonce: require('crypto').randomBytes(8).toString('hex'),
			user: btoa(JSON.stringify(req.user)),
			friend: btoa(JSON.stringify(users[friendname])),
			csrf: await res.generateCsrf()
		});
	}));

	fastify.get('/addfriend', auth(async (req, res) => {
		return res.view('addfriend', { csrf: await res.generateCsrf() });
	}));

	fastify.post('/addfriend', {
		preHandler: fastify.csrfProtection
	}, auth((req, res) => {
		const resKey = req.body['g-recaptcha-response'];
		const secretKey = '[REDACTED SECRET KEY]';
		var verificationUrl = "https://www.google.com/recaptcha/api/siteverify?secret=" + secretKey + "&response=" + req.body['g-recaptcha-response'];

		request(verificationUrl,function(error,response,body) {
			if(error) {
				return res.send("Unknown error!");
			}

			body = JSON.parse(body);
			if(body.success !== undefined && !body.success) {
				return res.send("Human Verification failed!");
			}		
			let { username,password } = req.body;
			if(addFriend.queue.length < 50) {
				addFriend.queue.push([username,password]);
				return res.send('Your friend request has been added to the queue, you are ' + addFriend.queue.length + " th in the queue.");
			}else{
				return res.send('The queue is currently at max capacity! Please try again later');
			}
		});
	}));
}) 

fastify.listen(8080, '0.0.0.0');

setInterval(() => {
	if(addFriend.queue.length == 0) return;
	var url = addFriend.queue.shift();
	addFriend.run(url[0],url[1]);
},5000);
