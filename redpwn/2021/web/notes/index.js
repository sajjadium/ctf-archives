const crypto = require('crypto');
const path = require('path');

const fastify = require('fastify')();

fastify.register(require('fastify-cookie'), {
  secret: process.env.FASTIFY_SECRET,
});

// handle some routes
fastify.register(require('./modules/api-plugin'), { prefix: '/api' });
fastify.register(require('./modules/routes-plugin'));
fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'public'),
  redirect: true,
});

fastify.listen(3000, '0.0.0.0');
