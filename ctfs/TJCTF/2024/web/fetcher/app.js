const express = require('express');
const fs = require('fs');
const app = express();

const flag = fs.readFileSync('flag.txt').toString();

app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/fetch', async (req, res) => {
    const url = req.body.url;

    if (!/^https?:\/\//.test(url))
        return res.send('invalid url');

    try {
        const checkURL = new URL(url);

        if (checkURL.host.includes('localhost') || checkURL.host.includes('127.0.0.1'))
            return res.send('invalid url');
    } catch (e) {
        return res.send('invalid url');
    }

    const r = await fetch(url, { redirect: 'manual' });

    const fetched = await r.text();

    res.send(fetched);
});

app.get('/flag', (req, res) => {
    if (req.ip !== '::ffff:127.0.0.1' && req.ip !== '::1' && req.ip !== '127.0.0.1')
        return res.send('bad ip');

    res.send(`hey myself! here's your flag: ${flag}`);
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
