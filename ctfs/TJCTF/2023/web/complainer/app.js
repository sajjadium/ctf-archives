const express = require('express');

const app = express();

app.use((req, res, next) => {
    console.log(req.method, req.url);
    next();
});

app.use('/static', express.static('public'));
app.set('view engine', 'ejs');

app.use('/api', require('./routes/api.js'));
app.use('/', require('./routes/web.js'));

app.listen(3000, () => {
    console.log('Server is up on port 3000.');
});
