const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const express = require('express');
const cookieParser = require('cookie-parser');
const yaml = require('yaml');

const yamlPath = path.join(__dirname, 'countries.yaml');
const countryData = yaml.parse(fs.readFileSync(yamlPath).toString());
const countries = new Set(Object.keys(countryData));
const countryList = JSON.stringify(btoa(JSON.stringify(Object.keys(countryData))));

const isoLookup = Object.fromEntries([...countries].map(name => [
  countryData[name].iso,
  {...countryData[name], name }
]));


const app = express();

const secret = crypto.randomBytes(32).toString('hex');
app.use(cookieParser(secret));

app.use('/assets', express.static(path.join(__dirname, 'assets')));

app.get('/switch', (req, res) => {
  if (!req.query.to) {
    res.status(400).send('please give something to switch to');
    return;
  }
  if (!countries.has(req.query.to)) {
    res.status(400).send('please give a valid country');
    return;
  }
  const country = countryData[req.query.to];
  if (country.password) {
    if (req.cookies.password === country.password) {
      res.cookie('iso', country.iso, { signed: true });
    }
    else {
      res.status(400).send(`error: not authenticated for ${req.query.to}`);
      return;
    }
  }
  else {
    res.cookie('iso', country.iso, { signed: true });
  }
  res.status(302).redirect('/');
});

app.get('/view', (req, res) => {
  if (!req.query.country) {
    res.status(400).json({ err: 'please give a country' });
    return;
  }
  if (!countries.has(req.query.country)) {
    res.status(400).json({ err: 'please give a valid country' });
    return;
  }
  const country = countryData[req.query.country];
  const userISO = req.signedCookies.iso;
  if (country.deny.includes(userISO)) {
    res.status(400).json({ err: `${req.query.country} has an embargo on your country` });
    return;
  }
  res.status(200).json({ msg: country.msg, iso: country.iso });
});

app.get('/', (req, res) => {
  const template = fs.readFileSync(path.join(__dirname, 'index.html')).toString();
  const iso = req.signedCookies.iso || 'US';
  const country = isoLookup[iso];
  res
    .status(200)
    .type('html')
    .send(template
      .replaceAll('$msg$', country.msg)
      .replaceAll('$name$', country.name)
      .replaceAll('$iso$', country.iso)
      .replaceAll('$countries$', countryList)
    );
});

app.listen(3000);
