const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const crypto = require('crypto');
const {msg, salt1, salt2, xs1, xs2, xs3} = require('./secret.js');

function sha1(salt1, salt2, salt3, msg) {
	let shasum = crypto.createHash('sha1');
	shasum.update(Buffer.from(salt1, 'base64'));
	shasum.update(msg);
	shasum.update(Buffer.from(salt2, 'base64'));
	shasum.update(Buffer.from(salt3, 'base64'));
	return shasum.digest('hex');
}

function getSalt3() {
	let time =  new Date().getTime();
	time /= 60 * 1000;
	time = Math.round(time);
	const s = `Time is ${time}`;
	const saltStr = `Salt:${sha1(xs1, xs2, xs3, s)}`;

	return Buffer.from(saltStr).toString('base64');
}

const app = express();
app.use(morgan('combined'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());

app.get("/", (req, res) => {
	res.send(`I Have the message: (${salt1}, ${salt2}, ${sha1(salt1, salt2, "", msg)}). Do you?`);
});

app.get("/s3", (req, res) => {
	res.send(`Salt3: ${getSalt3()}`);
});

app.post('/msg', (req, res) => {
	try {
		const {s1, s2, h} = req.body;
		if (typeof s1 != 'string' || typeof s2 != 'string' || typeof h != 'string') {
			res.send(`I knew it! You don't have it!`);
			return;
		}

		if (s1 == salt1 || s2 == salt2) {
			res.send(`I knew it! You don't have it!`);
			return;
		}

		const q = getSalt3();
		const v = sha1(s1, s2, q, msg);
		if (v != h) {
			res.send(`I knew it! You don't have it!`);
			return;
		}

		res.send(`Wow, you have it! Flag: ${msg}`);
	} catch(e) {
		res.send(`I knew it! You don't have it!`);
	}
});

app.listen(1337);
