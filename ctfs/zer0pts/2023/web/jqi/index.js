import fs from 'node:fs/promises';

import Fastify from 'fastify';
import jq from 'node-jq';

const fastify = Fastify({
    logger: true
});

const indexHtml = await fs.readFile('./index.html');
fastify.get('/', async (request, reply) => {
    reply.type('text/html').send(indexHtml);
});

const KEYS = ['name', 'tags', 'author', 'flag'];
fastify.get('/api/search', async (request, reply) => {
    const keys = 'keys' in request.query ? request.query.keys.toString().split(',') : KEYS;
    const conds = 'conds' in request.query ? request.query.conds.toString().split(',') : [];

    if (keys.length > 10 || conds.length > 10) {
        return reply.send({ error: 'invalid key or cond' });
    }

    // build query for selecting keys
    for (const key of keys) {
        if (!KEYS.includes(key)) {
            return reply.send({ error: 'invalid key' });
        }
    }
    const keysQuery = keys.map(key => {
        return `${key}:.${key}`
    }).join(',');

    // build query for filtering results
    let condsQuery = '';

    for (const cond of conds) {
        const [str, key] = cond.split(' in ');
        if (!KEYS.includes(key)) {
            return reply.send({ error: 'invalid key' });
        }

        // check if the query is trying to break string literal
        if (str.includes('"') || str.includes('\\(')) {
            return reply.send({ error: 'hacking attempt detected' });
        }

        condsQuery += `| select(.${key} | contains("${str}"))`;
    }

    let query = `[.challenges[] ${condsQuery} | {${keysQuery}}]`;
    console.log('[+] keys:', keys);
    console.log('[+] conds:', conds);

    let result;
    try {
        result = await jq.run(query, './data.json', { output: 'json' });
    } catch(e) {
        return reply.send({ error: 'something wrong' });
    }

    if (conds.length > 0) {
        reply.send({ error: 'sorry, you cannot use filters in demo version' });
    } else {
        reply.send(result);
    }
});
  
fastify.listen({ host: '0.0.0.0', port: 3000 }, (err, address) => {
    if (err) {
        fastify.log.error(err);
        process.exit(1);
    }
    console.log(`Server is now listening on ${address}`);
});