const {promises: fs} = require('fs');
const crypto = require('crypto');
const fastify = require('fastify');

const app = fastify();
app.register(require('fastify-cookie'));
app.register(require('fastify-session'), {
	secret: Math.random().toString(2),
	cookie: {secure: false},
});

const sessions = new Map();

const setRoutes = async (session, salt) => {
	const index = await fs.readFile('index.html');

	session.routes = {
		flag: () => '*** CENSORED ***',
		index: () => index.toString(),
		scrypt: (input) => crypto.scryptSync(input, salt, 64).toString('hex'),
		base64: (input) => Buffer.from(input).toString('base64'),
		set_salt: async (salt) => {
			session.routes = await setRoutes(session, salt);
			session.salt = salt;
			return 'ok';
		},
		[salt]: () => salt,
	};

	return session.routes;
};

app.get('/', async (request, reply) => {
	if (!sessions.has(request.session.sessionId)) {
		sessions.set(request.session.sessionId, {});
	}

	const session = sessions.get(request.session.sessionId);

	if (!session.salt) {
		session.salt = '';
	}
	if (!session.routes) {
		await setRoutes(session, '');
	}

	const {action, data} = request.query || {};

	let route;
	switch (action) {
		case 'Scrypt': route = 'scrypt'; break;
		case 'Base64': route = 'base64'; break;
		case 'SetSalt': route = 'set_salt'; break;
		case 'GetSalt': route = session.salt; break;
		default: route = 'index'; break;
	}

	reply.type('text/html')
	return session.routes[route](data);
});

app.listen(59101, '0.0.0.0');
