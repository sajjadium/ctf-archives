const express = require('express');
const jpv = require("jpv");
const jwt = require("jwt-simple");
const path = require("path");
const router = express.Router();

const config = require('../config');

const pattern = {
  firstName: /^\w{1,30}$/,
  lastName: /^\w{1,30}$/,
  passport: /^[0-9]{9}$/,
  ffp: /^(|CA[0-9]{8})$/,
  extras: [
    {sssr: /^(BULK|UMNR|VGML)$/},
  ],
};

function isSpecialCustomer(passport, frequentFlyerNumber) {
  return false;
}

function createToken(passport, frequentFlyerNumber) {
  var status = isSpecialCustomer(passport, frequentFlyerNumber) ? "gold" : "bronze";
  var body = {"status": status, "ffp": frequentFlyerNumber};
  return jwt.encode(body, config.privkey, 'RS256');
}

router.get('/', function(req, res, next) {
  res.sendFile('index.html', { root: path.join(__dirname, '../public') });
});

router.post('/checkin', function(req, res, next) {
  if (!req.body) return res.sendStatus(400);
  var data = req.body;
  
  if (jpv.validate(data, pattern, { debug: true, mode: "strict" })) {
    if (data["firstName"] == "Tony" && data["lastName"] == "Abbott") {
      var response = {msg: "You have successfully checked in! Please remember not to post your boarding pass on social media."};
    } else if (data["ffp"]) {
      var response = {msg: "You have successfully checked in. Thank you for being a Cr0wnAir frequent flyer."};
      for(e in data["extras"]) {
        if (data["extras"][e]["sssr"] && data["extras"][e]["sssr"] === "FQTU") {
          var token = createToken(data["passport"], data["ffp"]);
          var response = {msg: "You have successfully checked in. Thank you for being a Cr0wnAir frequent flyer. Your loyalty has been rewarded and you have been marked for an upgrade, please visit the upgrades portal.", "token": token};
        }
      }
    } else {
      var response = {msg: "You have successfully checked in!"};
    }
  } else {
    var response = {msg: "Invalid checkin data provided, please try again."};
  }

  res.json(response);
});

module.exports = router;

