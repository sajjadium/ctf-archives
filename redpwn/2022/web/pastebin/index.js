const crypto = require('crypto');
const express = require('express');
const app = express();

const pastes = new Map();
const add = (paste) => {
  const id = crypto.randomBytes(16).toString('hex');
  pastes.set(id, paste);
  return id;
};

app.use(require('body-parser').urlencoded({ extended: false }));

app.use((_req, res, next) => {
  res.set('set-cookie', `error=;expires=Thu, 01 Jan 1970 00:00:01 GMT`);
  next();
});

app.get('/', (req, res) => {
  const error = req.headers?.cookie?.match(/(?:^|; )error=(.+?)(?:;|$)/)?.[1];
  res.type('html');
  res.end(`
    <link rel="stylesheet" href="/style.css" />
    <div class="container">
        <h1>Yet Another Pastebin</h1>
        <form id="form" method="POST" action="/new">
            <textarea form="form" name="paste"></textarea>
            <input type="submit" value="Submit" />
        </form>
        <div style="color: red">${error ?? ''}</div>
    </div>
  `);
});

app.post('/new', (req, res) => {
  const paste = (req.body.paste ?? '').toString();

  if (paste.length == 0) {
    return res.redirect(`/flash?message=Paste cannot be empty!`);
  }

  if (paste.search(/<.*>/) !== -1) {
    return res.redirect(`/flash?message=Illegal characters in paste!`);
  }

  const id = add(paste);
  res.redirect(`/view/${id}`);
});

app.get('/flash', (req, res) => {
  const message = req.query.message ?? '';
  res.set('set-cookie', `error=${message}`);
  res.redirect('/');
});

app.get('/view/:id', (req, res) => {
  const id = req.params.id;
  res.type('html');
  res.end(`
    <link rel="stylesheet" href="/style.css" />
    <div class="container">
        <h1>Paste</h1>
        ${pastes.get(id) ?? 'Paste does not exist!'}
    </div>
  `);
});

app.get('/style.css', (_req, res) => {
  res.end(`
    * {
        font-family: 'Helvetica Neue', sans-serif;
        box-sizing: border-box;
    }

    html, body { margin: 0; }

    .container {
        padding: 2rem;
        width: 90%;
        max-width: 900px;
        margin: auto;
    }

    textarea {
      width: 100%;
      padding: 8px;
      margin: 8px 0;
      resize: vertical;
    }
  `);
});

app.listen(3000);
