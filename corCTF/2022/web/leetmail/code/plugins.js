import formBody from '@fastify/formbody'
import pointOfView from 'point-of-view';
import cookie from '@fastify/cookie'
import session from '@fastify/session'
import csrf from '@fastify/csrf-protection';
import ejs from 'ejs'
import crypto from 'crypto'
import path from 'path'
import { URL } from 'url';

export default fastify => {
    fastify.register(formBody);
    fastify.register(pointOfView, {
        engine: { ejs },
        root: path.join(new URL('.', import.meta.url).pathname, 'views')
    });
    fastify.register(cookie);
    fastify.register(session, {
        secret: crypto.randomBytes(32).toString('hex'),
        cookie: {
            secure: false
        }
    });
    fastify.register(csrf, { sessionPlugin: '@fastify/session' });
}