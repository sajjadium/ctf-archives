import fs from 'fs';
import express from 'express';
import log from './utils/logger.js';
import { createClient } from 'redis';
import handleHealthRequest from './routes/health.js';
import handleScreenshotRequest from './routes/screenshot.js';
import validateScreenshotRequest from './middlewares/validate-screenshot-request.js';
import { addProofOfWorkChallenge, validateProofOfWork } from './middlewares/proof-of-work.js';

if (!process.env.FLAG) {
    throw new Error('FLAG is not set');
}

async function main() {
    const port = 8080;
    const server = express();

    // write flag to disk
    fs.writeFileSync('/tmp/flag.txt', process.env.FLAG);

    // connect and add redis client to each request
    const redis = createClient({ url: "redis://redis:6379" });
    redis.on('error', (err) => console.log('[!] redis error', err));
    await redis.connect();

    server.use((req, _, next) => {
        req.redis = redis;
        next();
    });

    // register routess
    server.use(express.static('public'));
    server.get('/health', handleHealthRequest);

    if (process.env.DEV) {
        // when running in dev mode, we remove the proof of work validation
        server.get('/screenshot', addProofOfWorkChallenge, validateScreenshotRequest, /*validateProofOfWork,*/ handleScreenshotRequest);
    } else {
        server.get('/screenshot', addProofOfWorkChallenge, validateScreenshotRequest, validateProofOfWork, handleScreenshotRequest);
    }

    // start server
    server.listen(port, function (err) {
        if (err) {
            throw err;
        }

        log(`🚀 Up & running at http://localhost:${port}/`);
    });
}

main();