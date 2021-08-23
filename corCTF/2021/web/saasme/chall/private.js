const fastify = require('fastify')();
const spawn = require('child_process').spawn;
const schema = require('./schema');

fastify.post('/curl', { schema }, (req, res) => {
	let url;
	try {
		url = new URL(req.body.url);
	} catch(e) {
		return res.status(400).send('Invalid URL!');
	}

	console.log('[CURL] Visiting', url);

	// set HOST to prevent SSRF
	let curl = spawn('curl', ['-H', '"Host: nossrfhere"', '-H', 'User-Agent: ssrf-bot', '-N', '--fail', url.href]);

	let running = true;

	let timeout = setTimeout(() => {
		if (running) process.kill(curl.pid);
	}, 5000)

	let response = [];

	curl.stdout.on('data', data => response.push(data));

	curl.on('close', code => {
		clearTimeout(timeout);
		running = false;

		console.log('[CURL] Exited with code', code);
		
		if (code > 0) {
			return res.send('Invalid URL!');
		}

		res.type('text/plain').send(Buffer.concat(response));
	});
});

fastify.listen(8001);
