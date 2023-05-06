const express = require('express');
const crypto = require('crypto');
const app = express();

// Load options/config
const DOMAIN = process.env.DOMAIN || 'localhost';
const PORT = parseInt(process.env.PORT || '3000');
const TLS = !!(process.env.TLS || false);
const DEBUG = !!(process.env.DEBUG || false);
const CACHE_TIME = parseInt(process.env.CACHE_TIME || '300');
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'devpw';
const flag = process.env.FLAG || 'shaktictf{dev_flag}';
const protocol = TLS ? 'https://' : 'http://';
const jsUrl = `${protocol}${DOMAIN}${PORT === 80 || PORT === 443 || (PORT === 8080 && DOMAIN !== 'localhost') ? '' : `:${PORT}`}/js/`;
let adminSession = crypto.randomBytes(32).toString('hex');

// We'll just store the reports in memory for a bit
const messages = new Map();

if (DEBUG) {
  // Log headers and body of the requests to stdout
  app.use(function (req, res, next) {
    const date = new Date().toTimeString().split(' ')[0];
    console.log(`${date}: ${req.method} ${req.url}`);
    let logHeaders = "";
    req.rawHeaders.forEach((header, idx) => {
      if (idx % 2) {
        logHeaders += header + "\n";
      } else {
        logHeaders += "\t" + header + ": ";
      }
    });
    console.log(logHeaders);
    if (req.body) {
      console.log(req.body.toString('utf-8'));
    }
    next();
  });
}

// Body and cookie parsers
app.use(require('cookie-parser')());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(require('body-parser').json());

// Protect admin route with CSP
// TODO: Is this the right way to do this? We found a CSP evaluator that said sometimes this can be bypassed
app.use('/admin', (req, res, next) => {
  res.set('Content-Security-Policy', `object-src 'none'; script-src ${jsUrl};`);
  next();
});

// Sensitive admin functionality
app.get('/flag', (req, res) => {
  if (req.cookies.session === adminSession) {
    res.json({ flag });
  } else {
    res.sendStatus(401);
  }
});

// Retrieve current user
app.get('/user', (req, res) => {
  if (req.cookies.session === adminSession) {
    res.json({ name: "admin", id: 0 });
  } else {
    res.json(null);
  }
});

// Retrive message by ID
app.get('/message/:id', (req, res) => {
  if (req.cookies.session !== adminSession) {
    return res.json(null);
  }

  if (!req.params.id) {
    res.json({ error: "No message ID specified" });
  } else if (messages.has(req.params.id)) {
    res.json(messages.get(req.params.id));
  } else {
    res.json(null);
  }
});

// For sending messages to the admin
app.post('/message', (req, res) => {

  // Error handling
  if (!req.body.message || typeof req.body.message !== 'string') {
    return res.status(400).json({ error: 'invalid or missing message' });
  }
  if (!req.body.email || typeof req.body.email !== 'string') {
    return res.status(400).json({ error: 'invalid or missing email' });
  }

  // Create and store the message by ID
  const id = crypto.randomBytes(32).toString('hex');
  messages.set(id, {
    message: req.body.message,
    email: req.body.email
  });

  // return the ID to the client
  res.json({ id });

  // delete messages after CACHE_TIME seconds
  setTimeout(() => {
    messages.delete(id);
  }, CACHE_TIME * 1000);

});

// So admin can login and get the session cookie
app.post('/admin-login', (req, res) => {
  if (req.body.password === ADMIN_PASSWORD) {
    adminSession = crypto.randomBytes(32).toString('hex');
    return res.cookie('session', adminSession, {
      path: '/',
      sameSite: 'strict',
      secure: TLS,
      httpOnly: true
    }).redirect('/admin');
  }
  res.sendStatus(401);
});

// TODO: express.static seems to allow relative paths, is this safe?
app.use('/', express.static('public'));

app.listen(PORT);
console.log(`Listening on port ${PORT}`);
