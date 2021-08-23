const fastify = require('fastify')();
const spawn = require('child_process').spawn;
const schema = require('./schema');
const queue = require('./queue');
const fetch = require('node-fetch');
const path = require('path');

fastify.register(require('fastify-static'), { root: path.join(__dirname, 'static') })

fastify.post('/curl', { schema }, async (req, res) => {
	let url;
	try {
		url = new URL(req.body.url);
	} catch(e) {
		return res.status(400).send('Invalid URL!');
	}

	if (url.protocol !== 'http:' && url.protocol !== 'https:') {
		return res.status(400).send('Invalid URL!');
	}

	return res.type('text/plain').send(await (await fetch('http://127.0.0.1:8001/curl', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			url: url.href
		})
	})).text());
});

fastify.post('/chrome', { schema }, async (req, res) => {
	if (!req.body.url.startsWith('http://') && !req.body.url.startsWith('https://')) {
		return res.status(400).send('Invalid URL!');
	}

	queue.add(req.body.url);

	res.send('Added to queue!');
});

fastify.post('/kill', (req, res) => {
	queue.kill();

	res.send('Killed browser!');
})

fastify.get("/flag", (req, res) => {
    res.type('text/plain').send("thanks!!");
});

fastify.listen(8000, '0.0.0.0');