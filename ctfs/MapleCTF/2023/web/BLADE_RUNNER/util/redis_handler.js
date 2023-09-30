const redis = require("redis");

const REDISHOST = process.env.redishost || 'redis';


/* INITIALIZE REDIS CLIENT */
const redisClient = redis.createClient({
    socket: {
        host: REDISHOST,
        port: 6379
    }
});

redisClient.on('error', (err) => console.log(`[${new Date()}] NODE SERVER: REDIS CLIENT - Error: ${err}`));

redisClient.connect().then(() => {
    console.log(`[${new Date()}] NODE SERVER: REDIS CLIENT - Succesfully connected to Redis server.`);
});

redisClient.on("error", function (err) {
    console.log(`[${new Date()}] NODE SERVER: REDIS CLIENT - Error: ${err}`);
});


async function insert_response(k,v) {
    try {
        await redisClient.set(k, v);
        return true;
    }
    catch {
        return false;
    }


}

async function read_response(param) {
    const val = await redisClient.get(param);
    if (val) {
        return val;
    } else return null;
   
}


module.exports = {
    insert_response,
    read_response
}