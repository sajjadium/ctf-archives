const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
app.use(cookieParser());

app.get('/', (req, res) => {
    // free xss, how hard could it be?
    res.end(req.query?.xss ?? 'welcome to impossible-xss');
});

app.get('/flag', (req, res) => {
    // flag in admin bot's FLAG cookie
    res.end(req.cookies?.FLAG ?? 'dice{fakeflag}');
});

app.listen(8080);
