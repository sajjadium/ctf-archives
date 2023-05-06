var express = require('express');
var request = require('request');
var querystring = require('querystring');

var router = express.Router();

if (process.env.NODE_ENV == 'local') { //set the environment value before your running this app
  require('dotenv').config();
}


var target = process.env.TARGET_HOST;
var test = process.env.TEST;



/* GET home page. */
router.get('/', function(req, res, next) {
  request({
    headers: req.headers,
    uri: `http://${target}/`,
  }, function(err, data){
    res.render('index', { title: 'apis' , data: data.body});
  });
  
});


router.get('/coin', function(req, res, next) {
  request({
        headers: req.headers,
        uri: `http://${target}/coin`,
      }).pipe(res);
  });

  router.get('/addsub', function(req, res, next) {
    request({
          
          uri: `http://${target}/addsub`,
          qs: {
            email: req.query.email,
          }
        }).pipe(res);
    });
  
module.exports = router;
