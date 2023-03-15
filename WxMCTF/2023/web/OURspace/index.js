process.env.NODE_ENV = "production";
const JWT_SECRET = process.env.JWT_SECRET ?? "dummy_secret"

const express = require('express');
const cookie = require('cookie-parser');
const bodyparser = require('body-parser');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const { research } = require('./research.js');

const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

const app = express();

app.use(express.json());
app.use(bodyparser.urlencoded({ extended: true }));
app.use(cookie());

app.set('view engine', 'ejs');

app.use('/', (req, res, next) => {
    if (req.cookies.authorization) {
        try {
            let userdata = jwt.verify(req.cookies.authorization, JWT_SECRET);
            prisma.user.findUnique({
                where: {
                    username: userdata.username
                }
            }).then(usr => {
                if (usr) {
                    req.user = usr;
                }
                next();
            }).catch(() => { next() });
        }
        catch {
            next();
        }
    }
    else {
        next();
    }
})

app.post('/research', (req, res) => {
    try {
        jwt.verify(req.body.csrf, JWT_SECRET);
    }
    catch {
        res.status(401).send('L');
        return;
    }
    let status = JSON.parse(fs.readFileSync('./status.json').toString());
    if (!req.body.url) {
        res.status(401).send('?_?');
    }
    else if (status.visiting || status.lastvisit + 60000 > Date.now()) {
        res.status(403).send('nein');
    }
    else {
        status.visiting = true;
        status.lastvisit = Date.now();
        fs.writeFileSync('./status.json', JSON.stringify(status));
        research(req.body.url);
        res.render('result');
    }
});

app.get('/research', (req, res) => {
    if(req.user) {
        res.render('research', {
            csrf: jwt.sign({csrf: Date.now()}, JWT_SECRET)
        });
    }
    else {
        res.redirect('/login');
    }
})

app.get('/result', (req, res) => {
    if (fs.existsSync('./image.png')) {
        res.setHeader('Cache-Control', 'max-age=60, must-revalidate');
        res.sendFile(__dirname + '/image.png');
    }
    else {
        res.status(404).send('patience young padawan');
    }
});

app.get('/profile', (req, res) => {
    if (req.user) {
        res.setHeader('Content-Security-Policy', `script-src 'none'`);
        res.render('profile', { flag: req.cookies.flag, profile: req.user.profile });
    }
    else {
        res.redirect('/login');
    }
});

app.post('/login', (req, res) => {
    if (req.body.username && req.body.password) {
        prisma.user.findUnique({
            where: {
                username: req.body.username
            }
        }).then(usr => {
            if (usr) {
                if (usr.password == req.body.password) {
                    let token = jwt.sign({ username: usr.username }, JWT_SECRET);
                    res.cookie('authorization', token, { httpOnly: true });
                    res.redirect('/profile');
                }
                else {
                    res.status(401).send('T_T');
                }
            }
            else {
                res.status(401).send('???????????????????');
            }
        }).catch(() => { res.status(500).send('u suck') });
    }
    else {
        res.status(401).send('fill out the form properly goddammit');
    }
})

app.get('/login', (req, res) => {
    if(!req.user) {
        res.render('login');
    }
    else {
        res.redirect('/profile');
    }
})

app.post('/register', (req, res) => {
    if (req.body.username && req.body.password && req.body.csrf) {
        try {
            jwt.verify(req.body.csrf, JWT_SECRET); //goes to catch if invalid
            prisma.user.create({
                data: {
                    username: req.body.username,
                    password: req.body.password,
                    profile: req.body.profile ?? "This user is too lazy to make a profile"
                }
            }).then(() => {
                res.redirect('/login');
            }).catch((err) => { 
                console.log(err)
                res.status(500).send(':fingers_crossed: - :point_up:') });
        }
        catch {
            res.status(400).send('clown');
        }
    }
    else {
        res.status(401).send(':angry:');
    }
});

app.get('/register', (req, res) => {
    if(!req.user) {
        res.render('register', {
            csrf: jwt.sign({csrf: Date.now()}, JWT_SECRET)
        });
    }
    else {
        res.redirect('/profile');
    }
})

app.get('/', (req, res) => {
    res.render('index', {user: req.user});
})

app.use('/', (req, res) => {
    res.status(404).send('dafuq u doin');
})

app.listen(3000, () => {
    console.log('server be runnin (port 3000)');
});
