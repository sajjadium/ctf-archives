const express = require('express');
const crypto = require('crypto');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser')
const Set = require("collections/set");

const app = express();

app.use(bodyParser.json())
app.use(cookieParser())


// hash a username
const hash = (username)=>{
    return crypto.createHash('sha1').update(username || "nothing").digest('hex');
}

// get hashed token from request
const grabHashedTokenFromReq = (req)=>{
    const {token} = req.cookies;
    return crypto.createHash('sha1').update(token || "nothing").digest('hex');
}

// mappings
let TOKEN_TO_USERS = {};
let USERS = new Set();
let USERS_TO_MESSAGES = {};

// initialize admin
const ADMIN_TOKEN = process.env.ADMIN_TOKEN;
TOKEN_TO_USERS[hash(ADMIN_TOKEN)] = "admin"
USERS.add("admin")
USERS_TO_MESSAGES[hash("admin")] = []

// register route
app.get('/api/register/:username', function(req, res) {
    const {username} = req.params;
    if (!/^[a-zA-Z0-9]+$/.test(username)) return res.send({success: false, msg: "invalid char"})
    if (username.length < 10) return res.send({success: false, msg: "too short"})
    if (USERS.has(username)) return res.send({success: false, msg: "already exists"})
    USERS.add(username);
    const token = crypto.randomUUID();
    TOKEN_TO_USERS[hash(token)] = username;
    // add a welcome message
    if (USERS_TO_MESSAGES[hash(username)] === undefined) USERS_TO_MESSAGES[hash(username)] = []
    USERS_TO_MESSAGES[hash(username)].push({sender: "bot", "message": "hello world!"});
    res.cookie("token", token)
    return res.send({success: true, token})
})

// send message route
app.post('/api/message/:receiver', function(req, res) {
    const {message} = req.body;
    let {receiver} = req.params;
    receiver = hash(receiver);
    const token = grabHashedTokenFromReq(req);
    if (TOKEN_TO_USERS[token] === undefined)
        return res.send({success: false, msg: "no such token"})
    if (USERS_TO_MESSAGES[receiver] === undefined) USERS_TO_MESSAGES[receiver] = []
    USERS_TO_MESSAGES[receiver].push({sender: TOKEN_TO_USERS[token], message});
    return res.send({success: true});
});

// get messages route
// messages are immediately deleted after they are viewed
// service worker at frontend store the message in browser
app.get('/api/messages/:user', function(req, res) {
    const token = grabHashedTokenFromReq(req);
    if (TOKEN_TO_USERS[token] === undefined)
        return res.send({success: false, msg: "no such token"});
    const username = hash(TOKEN_TO_USERS[token]);
    const messages = USERS_TO_MESSAGES[username];
    // remove all messages
    USERS_TO_MESSAGES[username] = [];
    return res.send({success: true, messages});
});

// purge account route
// remove all messages in the account
app.get('/api/message/clear', function(req, res) {
    const token = grabHashedTokenFromReq(req);
    if (TOKEN_TO_USERS[token] === undefined)
        return res.send({success: false});
    const username = hash(TOKEN_TO_USERS[token]);
    USERS_TO_MESSAGES[username] = []
    return res.send({success: true});
});


app.listen(80)
