const express       = require('express');
const app           = express();
const routes        = require('./routes');
const path          = require('path');
const session       = require('express-session');
const randomize     = require('randomatic');

app.use(express.json());
app.set('views', './views');
app.use('/static', express.static(path.resolve('static')));

app.use(session({
	name: 'session',
	secret: randomize('aA0', 69),
	resave: false,
	saveUninitialized: false,
	cookie: { secure: true }
}));

app.use((req, res, next) => {
	if (req.session.auth == null) {
		req.session.auth = {
			'user': req.connection.remoteAddress == '127.0.0.1' ? 'admin' : 'guest'
		}
	}
	next();
});

app.use(routes);

app.all('*', (req, res) => {
    return res.status(404).send('404 page not found');
});

app.listen(1337, () => console.log('Listening on port 1337'));