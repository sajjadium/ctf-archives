const express = require('express');
const http = require('http');
const fs = require('fs');
const fast_convert = require('./build/Release/fast_convert.node');

const app = express();
const server = http.Server(app);

app.use(express.json());
app.use(express.urlencoded({ extended: true }))
app.use(express.static('public'))

app.get('/', (err, res) => {
  res.sendFile('./public/index.html')
});

app.get('/debug', (err, res) => {
  res.setHeader('content-type', 'text/plain');

  fs.readFile('/proc/self/maps', (err, data) => {
    if (err) {
      res.status(500);
      res.end('Internal Server Error');
    }
    else {
      res.end(data);
    }
  });
});

app.post('/hex_to_base64', (req, res) => {
  console.log(req.body);
  let { data } = req.body;

  if (!data || typeof data != 'string' || data.length % 2 != 0) {
    res.status(400);
    res.end('Bad Request');
    return;
  }

  const valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
  for (let i = 0; i < data.length; ++i) {
    if (valid_chars.indexOf(data[i]) == -1) {
      res.status(400);
      res.end('Bad Request');
      return;
    }
  }

  out = { data: fast_convert.hex_to_base64(data) };
  console.log(out);

  res.json(out);
});

app.post('/base64_to_hex', (req, res) => {
  console.log(req.body);
  let { data } = req.body;

  if (!data || typeof data != 'string') {
    res.status(400);
    res.end('Bad Request');
    return;
  }

  const valid_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890+/=';
  for (let i = 0; i < data.length; ++i) {
    if (valid_chars.indexOf(data[i]) == -1) {
      res.status(400);
      res.end('Bad Request');
      return;
    }
  }

  out = { data: fast_convert.base64_to_hex(data) };
  console.log(out);

  res.json(out);
});

console.log("[*] server running on port: 8080");
server.listen(8080);

