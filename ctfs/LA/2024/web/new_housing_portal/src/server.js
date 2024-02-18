const crypto = require('crypto');
const express = require('express');
const cookieParser = require('cookie-parser');

const app = express();

const secret = process.env.SECRET || crypto.randomBytes(32).toString('hex');

app.use(cookieParser(secret));
app.use(express.urlencoded({ extended: false }));

const users = new Map();

app.use((req, res, next) => {
  res.locals.user = users.get(req.signedCookies.auth) ?? null;
  next();
});

const needsLogin = (req, res, next) => {
  if (!res.locals.user) {
    res.redirect('/login/?err=' + encodeURIComponent('login required'));
    next();
  }
  next();
}

users.set('samy', {
  username: 'samy',
  name: 'Samy Kamkar',
  deepestDarkestSecret: process.env.FLAG || 'lactf{test_flag}',
  password: process.env.ADMINPW || 'owo',
  invitations: [],
  registration: Infinity
});

app.post('/register', (req, res) => {
  const username = req.body.username?.trim();
  const password = req.body.password?.trim();
  const name = req.body.name?.trim();
  const deepestDarkestSecret = req.body.deepestDarkestSecret?.trim();

  if (users.has(username)) {
    res.redirect('/login/?err=' + encodeURIComponent('username already exists'));
    return;
  }
  
  const user = {
    username,
    name,
    password,
    deepestDarkestSecret: 'todo',
    invitations: [],
    registration: Date.now()
  };

  users.set(username, user);
  res
    .cookie('auth', username, { signed: true, httpOnly: true })
    .redirect('/');
});

app.post('/login', (req, res) => {
  const username = req.body.username?.trim();
  const password = req.body.password?.trim();

  if (!users.has(username)) {
    res.redirect('/login/?err=' + encodeURIComponent('username does not exist'));
    return;
  }

  if (users.get(username).password !== password) {
    res.redirect('/login/?err=' + encodeURIComponent('incorrect password'));
    return;
  }

  res
    .cookie('auth', username, { signed: true, httpOnly: true })
    .redirect('/');
});

app.post('/finder', needsLogin, (req, res) => {
  const username = req.body.username?.trim();

  if (!users.has(username)) {
    res.redirect('/finder?err=' + encodeURIComponent('username does not exist'));
    return;
  }

  users.get(username).invitations.push({
    from: res.locals.user.username,
    deepestDarkestSecret: res.locals.user.deepestDarkestSecret
  });

  res.redirect('/finder?msg=' + encodeURIComponent('invitation sent!'));
});

app.get('/user', (req, res) => {
  const query = req.query.q;

  if (!users.has(query)) {
    res.json({ err: 'username not found' });
    return;
  }

  const { username, name } = users.get(query);

  res.json({ username, name });
});

app.get('/invitation', needsLogin, (req, res) => {
  res.json({ invitations: res.locals.user.invitations });
});

app.get('/', needsLogin);
app.get('/finder', needsLogin);
app.get('/request', needsLogin);

app.use('/', express.static(__dirname));

app.listen(3000, () => console.log('http://localhost:3000'));
