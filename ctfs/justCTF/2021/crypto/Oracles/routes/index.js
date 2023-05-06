var express = require('express');
var router = express.Router();
var asmCrypto = require('asmcrypto.js');
var b64 = require('base64url');
var fs = require('fs');

const key_params = fs.readFileSync('./oracles_stuff/key').toString().split(/\r?\n/);

const pubKey = [
  asmCrypto.hex_to_bytes(key_params[0]),
  asmCrypto.hex_to_bytes(key_params[1])
];

const privkey = [
  asmCrypto.hex_to_bytes(key_params[0]),
  asmCrypto.hex_to_bytes(key_params[1]),
  asmCrypto.hex_to_bytes(key_params[2]),
  asmCrypto.hex_to_bytes(key_params[3]),
  asmCrypto.hex_to_bytes(key_params[4]),
  asmCrypto.hex_to_bytes(key_params[5]),
  asmCrypto.hex_to_bytes(key_params[6]),
  asmCrypto.hex_to_bytes(key_params[7]),
];


const oraclePythia = new asmCrypto.RSA_OAEP(pubKey, new asmCrypto.Sha256(), fs.readFileSync('./oracles_stuff/Pythia'));
const oracleDodona = new asmCrypto.RSA_OAEP(pubKey, new asmCrypto.Sha256(), fs.readFileSync('./oracles_stuff/Dodona'));
const oracleIthlinne = new asmCrypto.RSA_OAEP(pubKey, new asmCrypto.Sha256(), fs.readFileSync('./oracles_stuff/Ithlinne'));

const TheQuestion1 = oraclePythia.encrypt(fs.readFileSync('./oracles_stuff/Goldbach'));
const TheQuestion2 = oracleDodona.encrypt(fs.readFileSync('./oracles_stuff/UltimateQuestion'));
const TheQuestion3 = oracleIthlinne.encrypt(fs.readFileSync('./oracles_stuff/flag'));


router.get('/', function(req, res, next) {
  res.render('index', {
    qP:b64.encode(TheQuestion1),
    qD:b64.encode(TheQuestion2),
    qI:b64.encode(TheQuestion3)
  });
});

router.get('/ask', function(req, res, next) {
  var oracleName = req.query.oracleName || 'Pythia';

  var question = req.query.question;
  if (question == undefined || question.length < 4) {
    res.render('index', {response: 'No question asked.'});
    return;
  }
  question = new Uint8Array(b64.toBuffer(question));

  const oracle = new asmCrypto.RSA_OAEP(privkey, new asmCrypto.Sha256(), fs.readFileSync('./oracles_stuff/' + oracleName));

  var response = 'I won\'t answer.';
  try {
      const result = oracle.decrypt(question);
      asmCrypto.bytes_to_string(result);
  } catch(err) {
      //
  }

  res.render('index', {response: response});
});


module.exports = router;
