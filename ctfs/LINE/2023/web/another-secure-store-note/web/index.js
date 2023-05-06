const fs = require('fs')
const ejs = require('ejs')
const path = require('path')
const crypto = require('crypto')
const express = require('express')
const cookieParser = require('cookie-parser')
const { db, createNewUser, getCsrf } = require('./db');

const app = express()

app.use('/', express.static(path.join(__dirname, 'public')))
app.use(express.urlencoded({extended: false}))
app.use(cookieParser())

function rand() { return crypto.randomBytes(20).toString('hex') }

app.use((req, res, next) => {
  const { id } = req.cookies;
  req.user = (id && db.cookies[id] && db.cookies[id].username) ? db.cookies[id].username : undefined;
  const csp = (id && db.cookies[id] && db.cookies[id].nonce) ? `script-src 'nonce-${db.cookies[id].nonce}'` : '';
  res.setHeader('Content-Security-Policy', `default-src 'self'; base-uri 'self'; ${csp}`)
  next()
})

function shouldBeLoggedIn(req, res, next) { if (!req.user) res.redirect('/'); else next(); }
function shouldNotBeLoggedIn(req, res, next) { if (req.user) res.redirect('/profile'); else next(); }
function csrfCheck(req, res, next) { 
  const { csrf } = req.body
  if (csrf !== getCsrf(req.cookies.id)) return res.redirect(`${req.path}?error=Wrong csrf`)
  next()
}

app.get('/', shouldNotBeLoggedIn, (req, res) => {
  res.render('auth.ejs')
})

app.post('/', shouldNotBeLoggedIn, csrfCheck, (req, res) => {
  const { username, password } = req.body
  try {
    if (db.users[username]) {
      if (db.users[username].password !== password) throw 'Wrong password';
    } else createNewUser(username, password)
    const newCookie = rand()
    db.cookies[newCookie] = Object.create(null)
    db.cookies[newCookie].username = username
    db.cookies[newCookie].csrf = rand()
    db.cookies[newCookie].nonce = rand()
    res.setHeader('Set-Cookie', `id=${newCookie}; HttpOnly; SameSite=None; Secure`)
    res.redirect('/profile')
  } catch (err) {
    res.redirect(`/?error=${err}`)
  }
})

app.get('/csp.gif', shouldBeLoggedIn, (req, res) => {
  db.cookies[req.cookies.id].nonce = rand()
  res.setHeader('Content-Type', 'image/gif')
  res.send('OK')
})

const settingsFile = fs.readFileSync('./views/getSettings.js', 'utf-8');
app.get('/getSettings.js', (req, res) => {
  res.setHeader('Content-Type', 'text/javascript');
  const response = ejs.render(settingsFile, { 
    csrf: getCsrf(req.cookies.id),
    domain: process.env.DOMAIN,
  });
  res.end(response);
})

app.get('/profile', shouldBeLoggedIn, (req, res) => {
  res.render('profile.ejs', { 
    name: db.users[req.user].name,
    nonce: db.cookies[req.cookies.id].nonce,
  });
})

app.post('/profile', shouldBeLoggedIn, csrfCheck, (req, res) => {
  const { name } = req.body;
  db.users[req.user].name = name;
  res.redirect('/profile?message=Successfully updated name')
})

// For interacting with admin bot
app.use('/bot', shouldBeLoggedIn, require('./bot.js'));

// We might need to change this to https in real challenge
const https = require('https');
const port = 4567
https
  .createServer({ 
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('cert.pem'),
  }, app)
  .listen(port, () => {
    console.log(`Server is runing at port ${port}`)
  });