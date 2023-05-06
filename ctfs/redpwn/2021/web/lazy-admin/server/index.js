const crypto = require('crypto');
const http = require('http');
const https = require('https');
const path = require('path');
const express = require('express');
const nunjucks = require('nunjucks');

const { multipartFormParser, validateURL, Database } = require('./util.js');

const db = new Database();
const app = express();

db.register('admin', {
  password: crypto.randomUUID(),
});

app.use(express.static(path.join(__dirname, 'public')));

// middleware to handle auth
app.use(require('cookie-parser')());
app.use((req, _res, next) => {
  if (!req.cookies?.token) {
    // our discord bot needs admin
    if (req.hostname === 'localhost') req.user = 'admin';
    return next();
  }
  req.user = db.getUsername(req.cookies.token);
  next();
});

// render some routes
nunjucks.configure(path.join(__dirname, 'views'), { express: app });
app.get('/', (req, res) => {
  if (req.user !== undefined) return res.redirect('/profile');
  res.render('index.njk', {
    layout: 'layout.njk',
    error: req.query.error,
  });
});

app.get('/contact', (_req, res) => {
  res.render('contact.njk', {
    layout: 'layout.njk',
  });
});

app.get('/admin', (_req, res) => {
  res.render('admin.njk', {
    layout: 'layout.njk',
  });
});

app.get('/profile', (req, res) => {
  if (req.user === undefined) return res.redirect('/');
  res.render('profile.njk', {
    layout: 'layout.njk',
    username: req.user,
    ...db.getInfo(req.user),
  });
});

// routes for logging in and registering
app.use(multipartFormParser);
app.post('/login', async (req, res) => {
  const shape = [
    ['username', 'field'],
    ['password', 'field'],
  ];

  const data = req.body;
  if (!data) return res.status(400).end();
  for (const [field, type] of shape) {
    if (type === 'any') continue;
    if (!data.get(field)) return res.status(400).end();
    if (data.get(field).type !== type) return res.status(400).end();
  }

  const { value: user } = data.get('username');
  const info = db.getInfo(user);
  if (!info || info.password !== data.get('password').value)
    return res.redirect('/?error=Incorrect username or password.');

  const token = db.login(user);
  return res.cookie('token', token, { maxAge: 900000 }).redirect('/profile');
});

app.post('/register', async (req, res) => {
  // registration is for admin only
  if (req.user !== 'admin') return res.status(400).end();

  const shape = [
    ['username', 'field'],
    ['password', 'field'],
    ['bio', 'field'],
    ['picture', 'any'],
  ];

  const data = req.body;
  if (!data) return res.status(400).end();
  for (const [field, type] of shape) {
    if (type === 'any') continue;
    if (!data.get(field)) return res.status(400).end();
    if (data.get(field).type !== type) return res.status(400).end();
  }

  const username = data.get('username').value;
  if (db.getInfo(username)) return res.status(400).end();

  const { value: pictureData, type: pictureType } = data.get('picture');

  let picture;
  const maxSize = 100000;
  if (pictureType === 'file') {
    if (pictureData.length > maxSize) picture = '';
    else picture = pictureData;
  } else {
    try {
      const { protocol, host, path, search } = JSON.parse(pictureData);

      // make sure there are no shenanigans
      const [success, ip] = await validateURL(protocol, host);
      if (!success) throw new Error('Invalid URL.');

      const options = {
        protocol,
        host: ip,
        path,
        search,
        headers: {
          Host: host,
        },
      };
      const data = new Promise((resolve, reject) => {
        let size = 0;
        const data = [];
        (options.protocol === 'http:' ? http : https)
          .get(options, (res) => {
            res.on('data', (chunk) => {
              if ((size += chunk.length > maxSize))
                reject(new Error('Image is too big!'));
              data.push(chunk);
            });
            res.on('end', () => resolve(Buffer.concat(data)));
          })
          .on('error', reject);
      });
      picture = await data;
    } catch {
      picture = '';
    }
  }
  picture = 'data:image/png;base64,' + picture.toString('base64');

  db.register(username, {
    password: data.get('password').value,
    bio: data.get('bio').value,
    picture,
  });

  return res.redirect('/admin');
});

// flag
app.get('/flag', (req, res) => {
  if (req.user === 'admin') return res.send(process.env.FLAG);
  res.status(400).end();
});

app.listen(80);
