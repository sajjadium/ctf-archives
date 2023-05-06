const express = require('express');
const crypto = require('crypto');
const app = express();

const adminPassword = crypto.randomBytes(16).toString('hex');

const bodyParser = require('body-parser');

app.use(require('cookie-parser')());

// don't let people iframe
app.use('/', (req, res, next) => {
  res.setHeader('X-Frame-Options', 'DENY');
  return next();
});

// sandbox the sandbox
app.use('/sandbox.html', (req, res, next) => {
  res.setHeader('Content-Security-Policy', 'frame-src \'none\'');
  // we have to allow this for obvious reasons
  res.removeHeader('X-Frame-Options');
  return next();
});

// serve static files
app.use(express.static('public/root'));
app.use('/login', express.static('public/login'));

// handle login endpoint
app.use('/ide/login', bodyParser.urlencoded({ extended: false }));

app.post('/ide/login', (req, res) => {
  const { user, password } = req.body;
  switch (user) {
  case 'guest':
    return res.cookie('token', 'guest', {
      path: '/ide',
      sameSite: 'none',
      secure: true
    }).redirect('/ide/');
  case 'admin':
    if (password === adminPassword)
      return res.cookie('token', `dice{${process.env.FLAG}}`, {
        path: '/ide',
        sameSite: 'none',
        secure: true
      }).redirect('/ide/');
    break;
  }
  res.status(401).end();
});

// handle file saving
app.use('/ide/save', bodyParser.raw({
  extended: false,
  limit: '32kb',
  type: 'application/javascript'
}));

const files = new Map();
app.post('/ide/save', (req, res) => {
  // only admins can save files
  if (req.cookies.token !== `dice{${process.env.FLAG}}`)
    return res.status(401).end();
  const data = req.body;
  const id = `${crypto.randomBytes(8).toString('hex')}.js`;
  files.set(id, data);
  res.type('text/plain').send(id).end();
});

app.get('/ide/saves/:id', (req, res) => {
  // only admins can view files
  if (req.cookies.token !== `dice{${process.env.FLAG}}`)
    return res.status(401).end();
  const data = files.get(req.params.id);
  if (!data) return res.status(404).end();
  res.type('application/javascript').send(data).end();
});

// serve static files at ide, but auth first
app.use('/ide', (req, res, next) => {
  switch (req.cookies.token) {
  case 'guest':
    return next();
  case `dice{${process.env.FLAG}}`:
    return next();
  default:
    return res.redirect('/login');
  }
});

app.use('/ide', express.static('public/ide'));

app.listen(3000);
