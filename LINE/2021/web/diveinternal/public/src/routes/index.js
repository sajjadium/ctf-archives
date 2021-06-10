var express = require('express');
const bodyParser = require('body-parser');
const path = require('path'); 


var router = express.Router();



router.use(express.static(path.join(__dirname, 'public')));


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('pages/index');
});



router.get('/subscribe', function(req, res, next) {
  res.render('pages/subscribe');
});

router.get('/about', function(req, res, next) {
  res.render('pages/about');
});



module.exports = router;
