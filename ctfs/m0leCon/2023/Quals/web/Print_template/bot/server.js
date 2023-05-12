const express = require('express')
const bot = require('./bot')

const {Semaphore} = require('async-mutex');

const BOT_SECRET = process.env.BOT_SECRET || 'changeme'
const MAX_PARALLEL_BOT = parseInt(process.env.MAX_PARALLEL_BOT) || 4

const semaphore = new Semaphore(MAX_PARALLEL_BOT);

const app = express()
app.use(express.json());

const MAX_QUEUE = 5
let inqueue = 0

app.post('/visit', async function (req, res) {
    
    if (req.body.secret !== BOT_SECRET){
        return res.status(500).json({ success: false, msg: 'bad secret' })
    }


    const url = req.body.url;
    if (typeof url === 'string' && /^https?:\/\/.+$/.test(url)) {
        try {

            if (inqueue > (MAX_QUEUE + MAX_PARALLEL_BOT)){
                console.error('Too many requests')
                return res.status(500).json({ success: false, msg: 'Too many requests to the bot, please retry later. If the problem persists contact an admin' });
            }

            inqueue ++
            console.log('QUEUE: ' + inqueue)
            console.log('Visiting: ' + url)

            semaphore.runExclusive(async ()=>{
                try { await bot.visit(url) } catch (e) {
                    console.error(e)
                }
                inqueue -- 
                console.log('QUEUE: ' + inqueue)
            })

            return res.json({ success: true, msg: 'A bot will visit your url' });
        } catch (e) {
            console.log(e);
            return res.status(500).json({ success: false, msg: 'failed' });
        }
    }
    res.status(400).json({ success: false, msg: 'bad url' });
})


app.listen(9999, '0.0.0.0');
