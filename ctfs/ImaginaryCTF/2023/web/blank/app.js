const express = require('express');
const session = require('express-session');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const crypto = require('crypto');
var fs = require("fs");
const path = require('path');

const app = express();
const port = 5000;

const db = new sqlite3.Database(':memory:');

db.serialize(() => {
  db.run('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)');
});

app.use(session({
  secret: crypto.randomBytes(16).toString('base64'),
  resave: false,
  saveUninitialized: true
}));

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.static('static'))
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  const loggedIn = req.session.loggedIn;
  const username = req.session.username;

  res.render('index', { loggedIn, username });
});

app.get('/login', (req, res) => {
  res.render('login');
});

app.post('/login', (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  db.get('SELECT * FROM users WHERE username = "' + username + '" and password = "' + password+ '"', (err, row) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error retrieving user');
    } else {
      if (row) {
        req.session.loggedIn = true;
        req.session.username = username;
        res.send('Login successful!');
      } else {
        res.status(401).send('Invalid username or password');
      }
    }
  });
});

app.get('/logout', (req, res) => {
  req.session.destroy();
  res.send('Logout successful!');
});

app.get('/flag', (req, res) => {
  if (req.session.username == "admin") {
    res.send('Welcome admin. The flag is ' + fs.readFileSync('flag.txt', 'utf8'));
  }
  else if (req.session.loggedIn) {
    res.status(401).send('You must be admin to get the flag.');
  } else {
    res.status(401).send('Unauthorized. Please login first.');
  }
});

app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
