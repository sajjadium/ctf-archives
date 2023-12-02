const express = require('express');
const app = express();
const bot = require('./bot');
const path = require('path');

app.use(express.urlencoded({ extended: false }));
app.use(express.static('static'))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'report.html'));
});


app.post('/', (req, res) => {
    const url = req.body.url
    if (url === undefined || (!url.startsWith('http://') && !url.startsWith('https://'))) {
        return res.status(400).send({ error: 'Invalid URL' })
    }

    return bot.visitPage(url)
        .then(() => res.send('Your submission is now pending review!'))
        //.catch((e) => res.send('Something went wrong! Please try again!'))
        .catch((e) => res.send(e.toString()));

});

(async () => {
    app.listen(8889, '0.0.0.0', () => console.log('Listening on port 8889'));
})();