const fastify = require('fastify')();

const path = require('path');

fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'public'),
  redirect: true,
  prefix: '/'
});

fastify.register(require('./routes/api'), {
  prefix: '/api/'
});

fastify.register(require('./routes/view'), {
  prefix: '/view/'
});

const start = async () => {
  console.log(`listening on ${await fastify.listen(3000, '0.0.0.0')}`)
}

start()
