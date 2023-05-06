import Fastify from 'fastify'
import plugins from './plugins.js'
import routes from './routes.js';

const fastify = Fastify({
    logger: true
});

plugins(fastify);
routes(fastify);

export default () => {
    fastify.listen({ port: 80, host: '0.0.0.0' });
}