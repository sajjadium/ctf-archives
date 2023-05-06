const crypto = require('crypto');
const express = require('express');

const db = require('better-sqlite3')('db.sqlite3');
db.exec(`DROP TABLE IF EXISTS users;`);
db.exec(`CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);`);
db.exec(`INSERT INTO users (username, password) VALUES (
    '${btoa('admin')}',
    '${btoa(crypto.randomUUID)}'
)`);

const app = express();

app.use(
  require('body-parser').urlencoded({
    extended: false,
  })
);

app.post('/login', (req, res) => {
  if (!req.body.username || !req.body.password)
    return res.redirect('/?message=Username and password required!');

  const query = `SELECT id FROM users WHERE
          username = '${req.body.username}' AND
          password = '${req.body.password}';`;
  try {
    const id = db.prepare(query).get()?.id;

    if (id) return res.redirect(`/?message=${process.env.FLAG}`);
    else throw new Error('Incorrect login');
  } catch {
    return res.redirect(
      `/?message=Incorrect username or password. Query: ${query}`
    );
  }
});

app.get('/', (req, res) => {
  res.send(`
  <div class="container">
    <h1>Sign In</h1>
    <form>
      <label for="username">Username</label>
      <input type="text" name="username" id="username" />
      <label for="password">Password</label>
      <input type="password" name="password" id="password" />
      <input type="submit" value="Submit" />
    </form>
    <div class="important">${(req.query.message ?? '')
      .toString()
      .replace(/>|</g)}</div>
  </div>
  <script>
    (async() => {
      await new Promise((resolve) => window.addEventListener('load', resolve));
      document.querySelector('form').addEventListener('submit', (e) => {
        e.preventDefault();
        const form = document.createElement('form');
        form.setAttribute('method', 'POST');
        form.setAttribute('action', '/login');

        const username = document.createElement('input');
        username.setAttribute('name', 'username');
        username.setAttribute('value',
          btoa(document.querySelector('#username').value)
        );

        const password = document.createElement('input');
        password.setAttribute('name', 'password');
        password.setAttribute('value',
          btoa(document.querySelector('#password').value)
        );

        form.appendChild(username);
        form.appendChild(password);

        form.setAttribute('style', 'display: none');

        document.body.appendChild(form);
        form.submit();
      });
    })();
  </script>
  <style>
    * {
      font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
      box-sizing: border-box;
    }

    html,
    body {
      height: 100%;
      margin: 0;
    }

    .container {
      padding: 2rem;
      width: 90%;
      max-width: 900px;
      margin: auto;
    }

    .important {
      color: red;
    }

    input:not([type='submit']) {
      width: 100%;
      padding: 8px;
      margin: 8px 0;
    }

    input[type='submit'] {
      margin-bottom: 16px;
    }
  </style>
  `);
});

app.use(function (err, req, res, next) {
  console.error(err);
  req.destroy();
});

app.listen(3000);
