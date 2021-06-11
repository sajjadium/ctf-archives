const express = require('express');
const morgan = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const db = require('./db.js');
const SqlString = require('sqlstring');

const {superSecretPassword, flag, salt} = require('./secret.js');

const md5 = (s) => {
	let hex = crypto.createHash('md5');
	hex.update(s);
	return hex.digest('hex');
};

const sign = (s) => {
	return md5(`${salt}${s}`);
};

const getCookie = (obj) => {
	const json = {
		...obj,
		secret: sign(obj.user),
	};
	const s = JSON.stringify(json);

	return Buffer.from(s).toString('base64');
};

const fromCookie = (cookie) => {
	try {
		const s = Buffer.from(cookie, 'base64').toString();
		const obj = JSON.parse(s);
		if (obj.secret !== sign(obj.user)) {
			return null;
		}
		return obj;
	} catch(e) {
		return null;
	}
};

const app = express();

app.use(morgan('combined'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
	res.send("Hack the planet");
});

app.post('/login', (req, res) => {
	const {user, pass, name} = req.body;

	if (user == null || name == null) {
		res.send("error");
		return;
	}

	if (user === 'admin' && pass !== superSecretPassword) {
		res.send("you're not the admin");
		return;
	}

	const cookie = getCookie({
		user,
		name: SqlString.escape(name),
	});
	
	const expires = new Date(Date.now() + 365 * 24 * 3600 * 1000);
	res.cookie('w1', cookie, {expires});
	res.send(`ok`);
});

app.get('/fetch', (req, res) => {
	const cookie = req.cookies.w1;
	if (cookie == null || cookie == "") {
		res.send("denied");
		return;
	}

	const session = fromCookie(cookie);

	if (session == null) {
		res.send("denied");
		return;
	}

	const name = req.query.name ? SqlString.escape(req.query.name) : session.name;

	const result = db.prepare(`SELECT user, token FROM secrets WHERE name=${name}`).get();

	if (result == null) {
		res.send("not found");
		return;
	}

	if (result.user != session.user) {
		res.send("denied");
		res.send(s);
		return;
	}

	if (result.user == 'admin' && md5(result.token) == '48bb6e862e54f2a795ffc4e541caed4d') {
		res.send(`you are clearly the admin: ${flag}`);
		return;
	}

	res.send("ok, bye");
});

app.listen(1337, () => {});
