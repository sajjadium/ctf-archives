var express = require('express');
var router = express.Router();


router.get('/', function(req, res, next) {
	console.log("index called")
 	res.render('index')
});

router.post('/admin', function(req, res, next) {
	var profile = req.body.profile
 	res.render('index', profile)
});

module.exports = router;