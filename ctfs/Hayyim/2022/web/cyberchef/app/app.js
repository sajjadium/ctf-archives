const express = require('express');
const bodyParser = require('body-parser');
const { checkRateLimit, checkUrl, visitUrl } = require('./utils');

const app = express();

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({
  extended: false
}));

app.get('/', (req, res) => {
  res.render('index');
});

app.post('/report', (req, res) => {
  const url = req.body.url;

  if (!checkUrl(url)) {
    res.redirect('/?message=invalid argument');
  } else if (!checkRateLimit(req.ip)) {
    res.redirect(`/?message=rate limited`);
  } else {
    visitUrl(url)
      .then(() => res.redirect('/?message=reported'));
  }
});

app.listen(8001);
