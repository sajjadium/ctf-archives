const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');

const nunjucks=require("nunjucks")

const routes = require('./routes');
const Database = require('./database');

const db = new Database(process.env.MYSQL_USER, process.env.MYSQL_PASSWORD, 'pinder');
db.connect();

const  app   = express();

const sessionParser = session({
    secret: process.env.SESSION_SECRET,
    resave: true,
    cookie: {
        httpOnly:true
    },
    saveUninitialized: true
})

app.use(sessionParser);
app.use(bodyParser.json());

app.use('/static', express.static('static'));
app.set('view engine', 'njk')
nunjucks.configure('views', {
    autoescape: true,
    express: app
})

app.use(routes(db, sessionParser));

app.all('*', (_, res) => {
    return res.status(404).send({
        message: '404 page not found'
    });
});

app.listen(80, () => console.log('Listening on port 3000'));