const express = require('express')
const bot = require('./bot')

const app = express()
app.use(express.json());


app.post('/visit', async function (req, res) {

    console.log(req.body);

    const url = req.body.url;
    if (typeof url === 'string' && /^https?:\/\/.+$/.test(url)) {
        try {
            bot.visit(url);
            return res.json({ msg: 'visited' });
        } catch (e) {
            console.log(e);
            return res.status(500).json({ error: 'failed' });
        }
    }
    res.status(400).json({ error: 'bad url' });
})


app.listen(9999, '0.0.0.0');
