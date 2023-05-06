const express = require('express');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
app.use(require('express-session')({'secret': fs.readFileSync('./sessionSecret').toString()}));
app.use(require('body-parser')({'extended': false}));

const sessions = {};

function newSession() {
  function Session() {
    this.isAdmin = false;
    this.checkSuperSecretStuff = function() {
      if (this.favourites === undefined || this.favourites.food === undefined) {
        return;
      }
      const something = this.favourites.food.toString() + fs.readFileSync('./flag.txt').toString();
      if (crypto.createHash('sha256').update(something).digest('hex') === '959c8b99849190a08b97968ca0968ca091908ba09ea08d9a9e93a099939e9882') {
        this.isAdmin = true;
      } else {
        this.isAdmin = false;
      }
    }
  }

  return new Session();
}

function getSession(req) {
  if (sessions[req.session.id] === undefined) {
    sessions[req.session.id] = newSession();
  }
  return sessions[req.session.id];
}

app.listen(3000);

app.get('/', (req, res) => {
  sess = getSession(req);
  if (!sess.is_admin) {
    // This seems conventional
    res.redirect('https://youtu.be/dQw4w9WgXcQ');
  } else {
    res.send('Congrabulations!<br><marquee><blink><b>' + fs.readFileSync("./flag.txt").toString() + '</b></blink></marquee>');
  }
});

function whatsThis(sess, k, v) {
  for (const p of k.split('.').slice(0, -1)) {
    if (sess[p] === undefined) {
      sess[p] = {};
    }
    sess = sess[p];
  }
  sess[k.split('.').pop()] = v;
}

app.put('/', (req, res) => {
  let sess = getSession(req);
  for (const k in req.body) {
    if (!k.split('.')[0].match(/admin/i)) {
        whatsThis(sess, k, req.body[k]);
    }
  }
  sess.checkSuperSecretStuff();
  res.send("Hmmm, if you say so...");
});
