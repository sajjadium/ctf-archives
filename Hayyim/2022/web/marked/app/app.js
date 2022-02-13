const crypto = require('crypto');
const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const md5 = require('md5');
const sanitizeHtml = require('sanitize-html');
const nodeHtmlParser = require('node-html-parser');
const marked = require('marked');

const { checkRateLimit, checkUrl, visitUrl, checkParam } = require('./utils');

const users = new Map();
const notes = new Map();

const app = express();

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(session({ secret: crypto.randomBytes(64).toString(), resave: false, saveUninitialized: true, }));

app.get('/', (req, res) => {
  res.redirect('/list');
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;

  if (!checkParam(username) || !checkParam(password)) {
    return res.redirect('/login?message=invalid argument');
  }

  if (!users.has(username)) {
    users.set(username, { username, password: md5(password), noteIds: new Array() });
  }

  if (users.get(username).password !== md5(password)) {
    return res.redirect('/login?message=invalid password');
  }

  req.session.username = username;
  res.redirect('/list');
});

app.get('/note/:noteId', (req, res) => {
  const { noteId } = req.params;

  if (!notes.has(noteId)) {
    return res.redirect('/list');
  }

  res.render('view', Object.assign(notes.get(noteId), { auth: true }));
});

app.get('/logout', (req, res) => {
  delete req.session.username;

  res.redirect('/login');
});

app.use((req, res, next) => {
  if (!req.session.username) {
    return res.redirect('/login');
  }

  req.session.login = users.get(req.session.username);
  next();
});

app.get('/list', (req, res) => {
  const { login } = req.session;
  const userNotes = login.noteIds.map(noteId => notes.get(noteId));

  res.render('list', { notes: userNotes, auth: true });
});

app.get('/new', (req, res) => {
  res.render('new', { auth: true });
});

app.post('/new', (req, res) => {
  const { login } = req.session;
  let { title, content } = req.body;

  if (!checkParam(title) || !checkParam(content)) {
    return res.redirect(`/list?message=invalid argument`);
  }

  /* convert markdown to html */
  const html = marked.parse(content);

  /* sanitize string as suggested by vendor
   * https://github.com/markedjs/marked/blob/96c46c75957fa6fbcd9153f29ac71322eb4c74b8/README.md#usage
   */
  const safeHtml = sanitizeHtml(html);

  /* remove unuseful <p> wrapper */
  const dom = nodeHtmlParser.parse(safeHtml);

  if (dom.childNodes.length === 2 && dom.firstChild.rawTagName === 'p' && dom.lastChild._rawText === '\n') {
    content = dom.firstChild.innerHTML;
  } else {
    content = dom.innerHTML;
  }

  if (typeof title !== 'string' || typeof content !== 'string' || title.length == 0 || content.length == 0 || title.length > 50 || content.length > 1000) {
    return res.redirect(`?message=invalid argument`);
  } 

  const noteId = md5(title + content);

  notes.set(noteId, { id: noteId, title, content });

  login.noteIds.push(noteId);

  users.set(login.username, login);

  res.redirect(`/list?message=successfully created`);
});

app.get('/report', (req, res) => {
  res.render('report', { auth: true });
});

app.post('/report', async (req, res) => {
  const { url } = req.body;

  if (!checkUrl(url)) {
    res.redirect(`?message=invalid argument`);
  } else if (!checkRateLimit(req.ip)) {
    res.redirect(`?message=rate limited`);
  } else {
    visitUrl(url)
      .then(() => res.redirect(`?message=reported`));
  }
});

app.listen(3000);
