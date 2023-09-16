const FLAG = process.env.FLAG ?? 'SECCON{dummy}';
const PORT = '3000';;

const express = require('express');
const cookieParser = require('cookie-parser');
const jwt = require('./jwt');

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

const secret = require('crypto').randomBytes(32).toString('hex');

app.use((req, res, next) => {
	try {
		const token = req.cookies.session;
		const payload = jwt.verify(token, secret);
		req.session = payload;
	} catch (e) {
		return res.status(400).send('Authentication failed');
	}
	return next();
})

app.get('/', (req, res) => {
	if (req.session.isAdmin === true) {
		return res.send(FLAG);
	} else {
		return res.status().send('You are not admin!');
	}
});

app.listen(PORT, () => {
	const admin_session = jwt.sign('HS512', { isAdmin: true }, secret);
	console.log(`[INFO] Use ${admin_session} as session cookie`);
  console.log(`Challenge server listening on port ${PORT}`);
});
