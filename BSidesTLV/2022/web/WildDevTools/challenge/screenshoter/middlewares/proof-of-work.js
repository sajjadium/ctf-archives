import crypto from 'crypto';
import log from '../utils/logger.js';

const DIFFICULTY = parseInt(process.env.DIFFICULTY) || 6;

function sha256(buf) {
    return crypto.createHash('sha256').update(buf).digest('hex');
}

export async function addProofOfWorkChallenge(req, res, next) {
    let puzzle = crypto.randomBytes(32).toString('hex');

    await req.redis.set(puzzle, DIFFICULTY, {
        EX: 90,
        NX: true
    });

    res.setHeader('X-PUZZLE', puzzle);
    res.setHeader('X-PUZZLE-EXPIRATION', 90);
    res.setHeader('X-DIFFICULTY', DIFFICULTY);

    next();
}

export async function validateProofOfWork(req, res, next) {
    let pow = req.headers['x-proof-of-work'],
        puzzle = req.headers['x-puzzle'];

    if (typeof pow !== 'string' || pow.length !== 32) {
        return res.status(400).json({ error: 'invalid X-PROOF-OF-WORK header' });
    }

    if (typeof puzzle !== 'string' || puzzle.length !== 64) {
        return res.status(400).json({ error: 'invalid X-PUZZLE header' });
    }

    log('pow', pow);
    log('puzzle', puzzle);

    try {
        const diff = await req.redis.sendCommand(['GETDEL', puzzle]);

        if (!diff) {
            throw 'puzzle not found';
        }

        if (diff != DIFFICULTY) {
            throw 'puzzle difficulty mismatch';
        }
    } catch (err) {
        log(err);
        return res.status(401).json({ error: 'expired or invalid puzzle' });
    }

    const buff = Buffer.concat([
        Buffer.from(puzzle),
        Buffer.from(pow, 'hex')
    ]);

    const hash = sha256(buff);

    if (!hash.startsWith('0'.repeat(DIFFICULTY))) {
        return res.status(401).json({ error: 'invalid proof of work solution' });
    }

    next();
}