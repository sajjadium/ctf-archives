const path = require('path');

const fastify = require('fastify')({
  logger: true,
});

// handle some routes
fastify.register(require('./modules/api-plugin'), { prefix: '/api' });
fastify.register(require('./modules/routes-plugin'));
fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'public'),
  redirect: true,
});

fastify.listen(3000, '0.0.0.0');
