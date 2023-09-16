const FLAG = process.env.FLAG ?? console.log('No flag') ?? process.exit(1);
const ADMIN_TOKEN = process.env.ADMIN_TOKEN ?? console.log('No admin token') ?? process.exit(1);

const PORT = '3000';

const express = require('express');
const rateLimit = require('express-rate-limit');
const cookieParser = require('cookie-parser');

const { visit } = require('./bot.js');

const reportLimiter = rateLimit({
  // Limit each IP to 1 request per 10 seconds
  windowMs: 10 * 1000, 
  max: 1, 
});

const app = express();

app.use((req, res, next) => {
  const js_url = new URL(`http://${req.hostname}:${PORT}/js/index.js`);
  res.header('Content-Security-Policy', `default-src ${js_url} 'unsafe-eval';`);
  next();
});

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.get('/flag', (req, res) => {
  if (req.cookies.token !== ADMIN_TOKEN || !req.get('X-FLAG')) {
    return res.send('No flag for you!');
  }
  return res.send(FLAG);
});

app.post('/report', reportLimiter, async (req, res) => {
  const { expr } = req.body;

  const url = new URL(`http://localhost:${PORT}/`)
  url.searchParams.append('expr', expr);

  try {
    await visit(url);
    return res.sendStatus(200);
  } catch (err) {
    console.error(err);
    return res.status(500).send('Something wrong');
  }
});

app.use('/', express.static('static'));

app.listen(PORT, () => {
  console.log(`Web server listening on port ${PORT}`);
});
