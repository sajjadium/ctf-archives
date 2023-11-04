const express = require('express');
const bodyParser = require('body-parser');
const routes = require('./routes');
const wsHandler = require('./wsHandler');
const db = require("./utils/db")
const cookieParser = require('cookie-parser');
const rateLimit = require('express-rate-limit')
const fs = require('fs')

const app = express();

db.init(app)
CHALL_URL = process.env.CHALL_URL ? process.env.CHALL_URL : "http://localhost:9011"
profilePerm = '{"profile":{"content_settings":{"exceptions":{"geolocation":{"'+CHALL_URL+',*":{"last_modified":"13343189901746175","last_visit":"13343097600000000","setting":1}}}}}}'
fs.writeFileSync('./profile/Default/Preferences', profilePerm)


const limiter = rateLimit.rateLimit({
	windowMs: 60, // 1 minute
	limit: 1800, // limit to 30 req/sec on 60 sec window
	standardHeaders: 'draft-7', // draft-6: `RateLimit-*` headers; draft-7: combined `RateLimit` header
	legacyHeaders: false, // Disable the `X-RateLimit-*` headers.
})

app.set('trust proxy', 1);
app.use(limiter)
app.use(bodyParser.json({type:"application/json",limit: "10mb"}));
app.use(cookieParser());
app.use('/static', express.static('static'))
app.set('view engine', 'ejs');
app.use(function(req, res, next) {
    res.setHeader('Content-Security-Policy', "script-src 'self'; style-src 'self';")
    next();
  });
  app.use(routes());

process.on('uncaughtException', function (err) {
    console.error(err);
});

server = require('http').createServer(app);
wsHandler.startHandler(server,app);
server.listen(9011, () => console.log('Listening on port 9011'));
