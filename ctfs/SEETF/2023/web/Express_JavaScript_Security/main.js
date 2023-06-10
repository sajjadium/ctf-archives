const express = require('express');
const ejs = require('ejs');

const app = express();

app.set('view engine', 'ejs');

const BLACKLIST = [
    "outputFunctionName",
    "escapeFunction",
    "localsName",
    "destructuredLocals"
]

app.get('/', (req, res) => {
    return res.render('index');
});

app.get('/greet', (req, res) => {
    
    const data = JSON.stringify(req.query);

    if (BLACKLIST.find((item) => data.includes(item))) {
        return res.status(400).send('Can you not?');
    }

    return res.render('greet', {
        ...JSON.parse(data),
        cache: false
    });
});

app.listen(3000, () => {
    console.log('Server listening on port 3000')
})