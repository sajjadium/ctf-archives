const fastify = require('fastify')();
const md = require('markdown-it')({
	html: true,
});

fastify.register(require('@fastify/static'), {
	root: require('path').join(__dirname, 'static')
});

fastify.addHook('preHandler', async (req, res) => {
	res.header('Content-Security-Policy', [
		"default-src 'self'",
		"base-uri 'self'",
		"font-src 'self'",
		"frame-ancestors 'none'",
		"img-src 'none'",
		"object-src 'none'",
		"script-src 'self' 'unsafe-eval' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/",
		"script-src-attr 'none'",
		"style-src 'self' 'unsafe-inline'",
		"frame-src https://www.google.com/recaptcha/ https://recaptcha.google.com/recaptcha/"
	].join(';'));

	res.header('X-Content-Type-Options', 'nosniff');
});

fastify.get('/render', {
	schema: {
		query: {
			type: 'object',
			properties: {
				content: {
					type: 'string',
					maxLength: 1000
				}
			},
			required: ['content']
		}
	}
}, (req, res) => {
	res.type('text/html').send(md.render(req.query.content));
});

fastify.listen(process.env.PORT || 3000);
