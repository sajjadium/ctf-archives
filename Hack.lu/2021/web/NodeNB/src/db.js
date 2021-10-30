const { promisify } = require("util");
const redis = require('redis');
const { nanoid } = require('nanoid/async');
const argon2 = require('argon2');

const REDIS_URL = process.env.REDIS_URL ?? 'redis://127.0.0.1:6379';
const FLAG = process.env.FLAG ?? 'fakeflag{dummy}';

const redisClient = redis.createClient({
    url: REDIS_URL,
});
redisClient.on('connect', () => {
    console.log('Connected to redis');
});
redisClient.on('error', (error) => {
    console.log('redis error:' + error?.message);
});

const db = {};
const asyncBinds = [
    'get', 'set', 'setnx', 'incr', 'exists', 'del',
    'hget', 'hset', 'hgetall', 'hmset', 'hexists',
    'sadd', 'srem', 'smembers', 'sismember',
];
for (const key of asyncBinds) {
    db[key] = promisify(redisClient[key]).bind(redisClient);
}

// init
db.hset('uid:1', 'name', 'system');
db.set('user:system', '1');
db.setnx('index:uid', 1);
db.hmset('note:flag', {
    'title': 'Flag',
    'content': FLAG,
});

const helpers = {
    async createUser(name, password) {
        const isAvailable = await db.setnx(`user:${name}`, 'PLACEHOLDER');
        if (!isAvailable) {
            throw new Error('user already exists!');
        }
        
        const uid = await db.incr('index:uid');
        await db.set(`user:${name}`, uid);

        const hash = await argon2.hash(password);
        await db.hmset(`uid:${uid}`, { name, hash });
        return uid;
    },
    async getUser(uid) {
        const user = await db.hgetall(`uid:${uid}`);
        if (!user) {
            return null;
        }
        user.id = uid;
        return user;
    },
    async getUserByNameAndPassword(name, password) {
        const uid = await db.get(`user:${name}`);
        if (!uid) {
            return null;
        }
        const user = await helpers.getUser(uid);
        if (!user) {
            return null;
        }
        try {
            if (await argon2.verify(user.hash, password)) {
                return user;
            } else {
                return null;
            }
        } catch (error) {
            console.log('argon error:', error?.message);
            return null;
        }
    },
    async getUserNotes(uid) {
        return db.smembers(`uid:${uid}:notes`);
    },
    async addNoteToUser(uid, nid) {
        return db.sadd(`uid:${uid}:notes`, nid);
    },
    async hasUserNoteAcess(uid, nid) {
        if (await db.sismember(`uid:${uid}:notes`, nid)) {
            return true;
        }
        if (!await db.hexists(`uid:${uid}`, 'hash')) {
            // system user has no password
            return true;
        }
        return false;
    },
    async deleteUser(uid) {
        const user = await helpers.getUser(uid);
        await db.set(`user:${user.name}`, -1);
        await db.del(`uid:${uid}`);
        const sessions = await db.smembers(`uid:${uid}:sessions`);
        const notes = await db.smembers(`uid:${uid}:notes`);
        return db.del([
            ...sessions.map((sid) => `sess:${sid}`),
            ...notes.map((nid) => `note:${nid}`),
            `uid:${uid}:sessions`,
            `uid:${uid}:notes`,
        ]);
    },
    async getUserSessions(uid) {
        return db.smembers(`uid:${uid}:sessions`);
    },
    async addSessionToUser(uid, sid) {
        return db.sadd(`uid:${uid}:sessions`, sid);
    },
    async removeSessionFromUser(uid, sid) {
        return db.srem(`uid:${uid}:sessions`, sid);
    },
    async createNote(title, content) {
        const nid = await nanoid();
        await db.hmset(`note:${nid}`, { title, content });
        return nid;
    },
    async getNote(nid) {
        const note = await db.hgetall(`note:${nid}`);
        note.id = nid;
        return note;
    },
};

module.exports = {
    redisClient,
    db: helpers,
};
