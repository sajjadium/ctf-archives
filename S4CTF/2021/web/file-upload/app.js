const express = require('express');
const morgan = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const path = require('path');

const {jwtSecret, flag} = require('./secret.js');
const {addToReviewLog, getReviewLog} = require('./admin.js');

const selfUrl = "http://file-upload.peykar.io/";

const multer  = require('multer');

const mimeMap = {
	'.jpg': 'image/jpeg',
	'.png': 'image/png',
	'.js': 'text/javascript',
	'.txt': 'text/plain',
};

const md5 = (s) => {
	let hex = crypto.createHash('md5');
	hex.update(s);
	return hex.digest('hex');
};

const storage = multer.diskStorage({
	destination: function (req, file, cb) {
		cb(null, './uploads/');
	},
	filename: function (req, file, cb) {
		const name = req.user.name;
		const oname = file.originalname || '';
		const rand = Math.round(Math.random() * 1E9);
		const hash = md5(`${oname}-${rand}`);

		const uniqueSuffix = Date.now() + '-' + hash;

		cb(null, `${name}-${uniqueSuffix}`);
	},
});

const upload = multer({ 
	storage,

	limits: {
		fileSize: 300 * 1024,
	},
});

const app = express();

app.use(morgan('combined'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use((req, res, next) => {
	req.user = {};

	const cookie = req.cookies['token'];
	if (cookie == null || cookie == "") {
		next();
		return;
	}

	try {
		const obj = jwt.verify(cookie, jwtSecret);
		req.user.name = obj.name;
	} catch(e) {
	}

	next();
});

app.get('/', (req, res) => {
	res.send(`<form method="get" action="/login">
	Username:
	<input type="text" name="user">
	<input type="submit" value="Login" />
</form>`);
});

app.get('/login/', (req, res) => {
	const {user} = req.query;

	if (typeof user != 'string') {
		res.send("no");
		return;
	}

	if (user === 'admin') {
		res.send("Wrong Password");
		return;
	}

	const token = jwt.sign({name: user}, jwtSecret);
	const expires = new Date(Date.now() + 365 * 24 * 3600 * 1000);
	res.cookie('token', token, {expires});
	res.send("Ok");
});

app.get('/files/:user/:token/:file', (req, res) => {
	const {user, token, file} = req.params;
	const ext = path.extname(file);
	const mime = mimeMap[ext];
	if (mime == null) {
		res.status(404);
		res.send("Not found");
		return;
	}

	res.set('Content-Type', mime);
	res.sendFile(`${user}-${token}`, {
		root: './uploads'
	});
});

app.use('/upload/', (req, res, next) => {
	if (!req.user || req.user.name == null) {
		res.send("please login first");
	} else {
		next();
	}
});

app.post('/upload/', upload.single('file'), (req, res) => {
	const token = req.file.filename.split('-').slice(1).join('-');
	res.json({
		token,
		addr: `/files/${req.user.name}/${token}/${req.file.originalname}`
	});
});

app.use('/report', async (req, res) => {
	if (!req.user || req.user.name == null) {
		res.send("denied");
		return;
	}

	if (req.method === 'POST') {
		const {url} = req.body;
		const q = await addToReviewLog(selfUrl + url); // admin will check the links
		res.send("admin will review the link shortly");
		return;
	}

	if (req.user.name !== "admin") {
		res.send(`<form method="post" action="/report">
		url: <br>
		${selfUrl}<input type="text" name="url" />
		<input type="submit" value="Report" />
	</form>`);
		return;
	}

	const urls = await getReviewLog();
	res.send(`
<html>
<body>
<h1>Flag: ${flag}</h1>
${urls.map(url => `<a href="${url}">${url}</a><br>`).join("\n")}
</body>
</html>
`);
});

app.listen(1337, () => {});
