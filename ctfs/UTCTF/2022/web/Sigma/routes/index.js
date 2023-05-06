var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { });
});

router.post('/', function(req, res, next) {
  const img = Buffer.from(req.body.image, 'base64').toString('base64');
  res.render('index', { img });
})

module.exports = router;
