const express = require('express');
const cookieParser = require('cookie-parser');
const app = express();
const port = 3000;

app.use(cookieParser());
app.use('/static', express.static('static'))
app.use((req, res, next) => {
    res.set("X-Frame-Options", "DENY");
    res.set(
      "Content-Security-Policy", 
      "style-src 'unsafe-inline'; script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.6/purify.min.js"
    );
    next();
  });
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/flag', (req, res) => {
    res.type('text/plain');
    const name = req.query.name || 'admin';
    if (typeof name !== 'string' || name.length > 32 || /[^\x00-\x7f]/.test(name)) {
        res.send('Invalid name!');
        return;
    }
    const flag = req.cookies.flag || 'n1ctf{[A-Za-z]+}';
    res.send(`${name} ${flag}`);
});

app.listen(port, '0.0.0.0', () => {
    console.log(`App listening at http://0.0.0.0:${port}`);
});