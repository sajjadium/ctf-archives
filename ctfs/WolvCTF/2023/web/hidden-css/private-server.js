const express = require('express');
const app = express();

const FLAG = 'wctf{redacted}'

// To visit me, please use a URL like http://0/css
// since http://localhost/css will NOT work.
app.get('/css', function(req, res) {
    let prefix = '' + req.query.prefix
    console.log('visit to /css?prefix='+prefix)
    for (c of prefix) {
        const charCode = c.charCodeAt(0)
        if (charCode < 32 || charCode > 126) {
            prefix = 'illegal characters seen'
            break
        }
    }

    if (prefix.length > 20) {
        prefix = 'your prefix is too long'
    }

    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Content-Type', 'text/css');
    res.send(prefix + FLAG);
});

const port = 1337;
app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})
