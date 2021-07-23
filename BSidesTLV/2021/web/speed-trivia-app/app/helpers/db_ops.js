const redis = require("redis");
const REDIS_PORT  = process.env.REDIS_PORT || 6379
const REDIS_HOST  = process.env.REDIS_HOST || 'localhost'
const DEFAULT_TTL = process.env.DEFAULT_TTL || 60*5
const NON_ZERO    = 1
const FIELDS = {
    LEVEL: 'level',
    SCORE: 'score'
};


const client = redis.createClient(REDIS_PORT, REDIS_HOST);
client.on("error", function(error) {
    console.error(`REDIS ERROR :: `, error);
});

async function new_game(gameId) {
    console.log(`${gameId} :: CREATING NEW GAME `);
    await client.hmset (`${gameId}:stats`, FIELDS.SCORE, NON_ZERO, FIELDS.LEVEL, NON_ZERO);
    await client.expire(`${gameId}:stats`, DEFAULT_TTL)
    return;
}

async function get_field(gameId, field) {
    console.log(`${gameId} :: GETTING ${field} `);
    return await new Promise( (resolve, reject) => {
        client.hmget(`${gameId}:stats`, field, async (err, res) => {
            console.log(`RES(${field}) :: `, res);
            if(res[0] >= NON_ZERO) {
                resolve(parseInt(res[0]));
            } else {
                resolve(0);
            }
            
        });
    }); 
}

async function incr_field(gameId, field, points) {
    console.log(`${gameId} :: INCREASING FIELD ${field} += ${points}`);
    return await new Promise( (resolve, reject) => {
        client.hincrby(`${gameId}:stats`, field, points, async (err, res) => {
            resolve(res);
        });
        return;
    }); 
}

const db = {
    FIELDS,
    new_game,
    get_field,
    incr_field
}

module.exports = { db, NON_ZERO, DEFAULT_TTL }