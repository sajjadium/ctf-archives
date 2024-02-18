const express = require('express');
const cookieParser = require('cookie-parser');
const fs = require('fs');

const FLAG = process.env.FLAG ?? 'lactf{this_is_a_flag}';
const ADMINPW = process.env.ADMINPW ?? 'owouwurawr';
const dev = !process.env.ADMINPW;

const app = express();

const users = new Map();

const choose = arr => arr[Math.floor(Math.random() * arr.length)];

const generateOTP = () => {
  const target = 80;
  const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const otp = Array(target)
    .fill('0')
    .map(() => choose(alphabet))
    .join('');
  if (otp.length === target) {
    return otp;
  }
  return generateOTP();
};

const quote = text => text.replaceAll('"', '&quot;');

app.use(cookieParser());

app.get('/flag', (req, res) => {
  if (!req.query.user) {
    res.status(400).send('Please specify a user');
    return;
  }
  if (!req.query.otp) {
    res.status(400).send('Please specify an otp');
    return;
  }
  const otp = users.get(req.query.user);
  users.delete(req.query.user);
  if (!otp || otp !== req.query.otp) {
    res.status(400).send('Incorrect otp');
    return;
  }
  res.status(200).send(FLAG);
});

app.get('/note.js', (req, res) => {
  const js = fs.readFileSync('note.js').toString();
  res
    .status(200)
    .header('Content-Type', 'text/javascript')
    .send(js);
});

app.get('/', (req, res) => {
  if (!req.query.user) {
    res.status(400).send('Please specify a user in the query!');
    return;
  }
  res
    .status(200)
    .header(
      'Content-Security-Policy',
      "font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; script-src 'self'; style-src 'unsafe-inline'"
    );

  const page = fs.readFileSync('note.html').toString();
  if (dev || req.cookies.token === ADMINPW) {
    const otp = generateOTP();
    users.set(req.query.user, otp);
    res.send(page.replaceAll('<PASSWORD>', quote(otp)));
    return;
  }
  res.send(page.replaceAll('<PASSWORD>', quote(generateOTP())));
});

app.listen(3000);
