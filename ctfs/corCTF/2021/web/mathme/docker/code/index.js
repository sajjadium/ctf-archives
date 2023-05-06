const express = require('express');
require('express-async-errors');
const bcrypt = require('bcryptjs');
const expressJWT = require('express-jwt');
const config = require('./config');
const cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');
const markdown = require('markdown-it')();
const fs = require('fs');

const { User, Note } = require('./models');
const { Liquid } = require('liquidjs');
const { validate } = require('express-jsonschema');

const app = express();

const engine = new Liquid();
app.engine('liquid', engine.express()); 
app.set('views', './templates');
app.set('view engine', 'liquid');

app.use(express.urlencoded({
	extended: false
}));

app.use(cookieParser());

app.use(expressJWT({ 
	secret: config.secret,
	algorithms: ['HS256'],
	getToken: (req) => {
		if (req.cookies.session) {
			return req.cookies.session;
		}

		return null;
	}
}).unless({ path: ['/', '/login', '/register'] }));

function issueSession(user) {
	return jwt.sign({
		id: user.id,
		username: user.username,
		exp: Math.floor(Date.now() / 1000) + (6 * 60 * 60)
	}, config.secret);
}

const userSchema = {
	type: 'object',
	properties: {
		username: {
			type: 'string',
			required: true,
			minLength: 1,
			maxLength: 60
		},
		password: {
			type: 'string',
			required: true,
			minLength: 1,
			maxLength: 60
		}
	}
};

const noteSchema = {
	type: 'object',
	properties: {
		title: {
			type: 'string',
			required: true,
			minLength: 1,
			maxLength: 255,
		},
		data: {
			type: 'string',
			required: true,
			minLength: 1,
			maxLength: 2 ** 16
		}
	}
}

const adminSchema = {
	type: 'object',
	properties: {
		url: {
			type: 'string',
			required: true
		}
	}
}

app.get('/', expressJWT({ 
	secret: config.secret,
	algorithms: ['HS256'],
	credentialsRequired: false,
	getToken: (req) => {
		if (req.cookies.session) {
			return req.cookies.session;
		}

		return null;
	}
}), (req, res) => {
	if (req.user) {
		return res.redirect('/notes');
	}

	return res.redirect('/login');
})

app.get('/login', (req, res) => res.render('login'));

app.post('/login', validate({ body: userSchema }), async (req, res) => {
	const user = await User.findOne({ where: { username: req.body.username } });

	if (user === null || !bcrypt.compareSync(req.body.password, user.password)) {
		return res.status(400).render('error', {	
			error: 'Invalid username or password.'
		});
	}
	
	return res.cookie('session', issueSession(user), { httpOnly: true }).redirect('/');
});

app.get('/register', (req, res) => res.render('register'));

app.post('/register', validate({ body: userSchema }), async (req, res) => {
	if (await User.count({ where: { username: req.body.username } })) {
		return res.status(400).render('error', {
			error: 'User already exists'
		});
	}

	const user = await User.create({
		username: req.body.username,
		password: bcrypt.hashSync(req.body.password, 12)
	});
	
	return res.cookie('session', issueSession(user), { httpOnly: true }).redirect('/');
});

app.get('/notes', async (req, res) => {
	const user = await User.findOne({ where: { id: req.user.id }, include: Note});

	return res.render('notes', {
		notes: user.notes
	});
});

app.get('/create', (req, res) => res.render('create'));

app.post('/create', validate({ body: noteSchema }), async (req, res) => {
	if (req.user.admin) {
		return res.status(400).render('error', {
			error: 'Note creation has been disabled for admin.'
		});
	}
	
	const note = await Note.create({
		userId: req.user.id,
		title: req.body.title,
		data: req.body.data
	});

	return res.redirect(`/note?id=${note.id}`);
});

app.get('/note', async (req, res) => {
	if (req.query.id === undefined) {
		return res.render('error', {
			error: 'Please specify a note id.'
		});
	}

	const note = await Note.findOne({
		where: {
			id: req.query.id.toString()
		}
	});

	if (note) {
		if (!req.user.admin && note.userId !== req.user.id) {
			return res.status(400).render('error', {
				error: 'Unauthorized'
			});
		}
		note.html = markdown.render(note.data);
	}

	return res.render('note', {
		note
	});
});

app.get('/flag', (req, res) => {
	if (!req.user.admin) {
		return res.status(400).send('Only admin can view the flag!');
	}
	res.send(fs.readFileSync('flag.txt', 'utf-8'));
});

app.use((err, req, res, next) => {	
	if (err.name === 'JsonSchemaValidation') {
		res.status(400).render('error', { error: 'Failed to validate request.' });
	} else if (err.name === 'UnauthorizedError') {
		res.clearCookie('session').redirect('/');
	} else {
		console.error(err);
		res.status(500).render('error', { error: 'Internal Server Error!' });
	}
});

app.listen(8000);