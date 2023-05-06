const express = require('express');
const jpv = require("jpv");
const jwt = require("jwt-simple");
const path = require("path");
const router = express.Router();

const config = require('../config');

function getLoyaltyStatus(req, res, next) {
  if (req.headers.authorization) {
    let token = req.headers.authorization.split(" ")[1];
    try {
      var decoded = jwt.decode(token, config.pubkey);
    } catch {
      return res.json({ msg: 'Token is not valid.' });
    }
    res.locals.token = decoded;
  }
  next()
}

router.get('/', function(req, res, next) {
  res.sendFile('upgrades.html', { root: path.join(__dirname, '../public') });
});

router.post('/legroom', [getLoyaltyStatus], function(req, res, next) {
  if (res.locals.token && ["bronze", "silver", "gold"].includes(res.locals.token.status)) {
    var response = {msg: "Upgrade successfully selected"};
  } else {
    var response = {msg: "You do not qualify for this upgrade at this time. Please fly with us more."};
  }
  res.json(response);
});

router.post('/toilets', [getLoyaltyStatus], function(req, res, next) {
  if (res.locals.token && ["bronze", "silver", "gold"].includes(res.locals.token.status)) {
    var response = {msg: "Upgrade successfully selected"};
  } else {
    var response = {msg: "You do not qualify for this upgrade at this time. Please fly with us more."};
  }
  res.json(response);
});

router.post('/flag', [getLoyaltyStatus], function(req, res, next) {
  if (res.locals.token && res.locals.token.status == "gold") {
    var response = {msg: config.flag };
  } else {
    var response = {msg: "You do not qualify for this upgrade at this time. Please fly with us more."};
  }
  res.json(response);
});

module.exports = router;

