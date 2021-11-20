const express = require('express');
const { timingSafeEqual } = require('crypto');


// TODO: What were we optimizing by using bitflags for the environments again?
// Note: values are 1, 2, 4, 8, 16, 32
const [ENV_PROD_EAST, ENV_PROD_WEST, ENV_STAGE_EAST, ENV_STAGE_WEST, ENV_DEV_EAST, ENV_DEV_WEST] =
      [0b000001,      0b000010,      0b000100,       0b001000,        0b010000,     0b100000];

// Unicode in the username makes it more secure, thankfully we can have unicode characters in source
const [USERNAME, PASSWORD] = ['root🚀', 'ROOT_PASSWORD_NOT_SHARED'];
const FLAG = 'FLAG_NOT_SHARED'

const app = express();
const ENVIRONMENT = '2'; // Note: We are deployed in production-west


function stringsEqual(str1, str2) {
  if (str1 === undefined || str2 === undefined || str1.length !== str2.length) {
    return false;
  }
  return timingSafeEqual(Buffer.from(str1, "utf8"), Buffer.from(str2, "utf8"));
}

app.get('/login', async (req, res) => {
    const {
      username,
      password,
   ㅤ} = req.query;

   // Note: Auth check here, only bypassable in staging or dev envs
    if ((stringsEqual(USERNAME, username) && stringsEqual(PASSWORD, password)) ||
        (+ENV_STAGE_EAST ==ㅤ+ENVIRONMENT || +ENV_STAGE_WEST ==ㅤ+ENVIRONMENT) ||
        (+ENV_DEV_EAST ==ㅤ+ENVIRONMENT || +ENV_DEV_WEST ==ㅤ+ENVIRONMENT)) {
      res.status(200);
      res.send(FLAG);
    } else {
      res.status(401);
      res.send('UNAUTHORIZED');
    }
});

app.get('/', async (req, res) => {
  res.status(200);
  res.send(`
  <html>
  <head><title>Korean Space Agency Login Portal</title></head>
  <style type="text/css">
  body{max-width: 800px; margin: 0 auto;}
  label{display: block;margin-bottom: 0.25em;}
  input{display:block;padding: 10px;width:100%;}</style>
  <body>
  <h1>Korean Space Agency Login Form 🚀</h1>
  <form action="/login" method="GET">
  <label for="username">Username:</label><input type="text" name="username"><br>
  <label for="password">Password:</label><input type="password" name="password"><br>
  <input type="submit">
  </form>
  </body>
  </html>
  `)
});

app.listen(8080, '0.0.0.0');
