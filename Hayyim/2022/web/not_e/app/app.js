const crypto = require('crypto');
const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');

const { Database, md5, checkParam } = require('./utils');

const app = express();
const db = new Database(':memory:');

app.set('view engine', 'ejs')

app.use(bodyParser.urlencoded({
  extended: false
}));

app.use(session({
  secret: crypto.randomBytes(32).toString()
}));

app.all('/login', async (req, res) => {
  if (req.method !== 'POST') {
    return res.render('login');
  }

  const { username, password } = req.body;

  if (!checkParam(username) || !checkParam(password)) {
    return res.redirect('?message=invalid argument');
  }

  const result = await db.get('select username, password from members where username = ?', [
    username
  ]);

  if (!result) {
    await db.run('insert into members values (?, ?)', [ username, md5(password) ]);
  } else if (result.password !== md5(password)) {
    return res.redirect('?message=incorrect password');
  }

  req.session.login = username;
  res.redirect('/');
});

app.use((req, res, next) => {
  if (!req.session.login) {
    res.redirect('/login');
  }

  next();
});

app.use('/logout', (req, res) => {
  delete req.session.login;

  res.redirect('/login');
});

app.get('/', async (req, res) => {
  const notes = await db.getAll('select * from posts where owner = ?', [ req.session.login ]);

  res.render('list', { notes, auth: true });
});

app.all('/new', async (req, res) => {
  if (req.method !== 'POST') {
    return res.render('new', { auth: true });
  }

  const { title, content } = req.body;

  if (!checkParam(title) || !checkParam(content)) {
    return res.redirect('?message=invalid argument');
  }

  const noteId = md5(title + content);

  await db.run('insert into posts values (?, ?, ?, ?)', [ noteId, title, content, req.session.login ]);

  return res.redirect('/?message=successfully created');
});

app.get('/view/:noteId', async (req, res) => {
  const { noteId } = req.params;
  const note = await db.get('select * from posts where id = ?', [ noteId ]);

  if (!note) {
    return res.redirect('/?message=invalid note');
  }

  res.render('view', { note, auth: true });
});

app.listen(1000);
