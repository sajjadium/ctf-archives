var express = require('express');
var cookieParser = require('cookie-parser');
var escape = require('escape-html');
var serialize = require('node-serialize');
var bodyParser = require('body-parser');
var app = express();
var path = require('path');
app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

app.get('/', (req,res) => {
	res.render('home.ejs');
});

app.post('/', (req,res) => {
	res.render('loggedin.ejs')
});

app.get('/guest', function(req, res) {
   res.render('guest.ejs');
});

app.post('/guest', function(req, res) {
   if (req.cookies.guest) {
   	var str = new Buffer(req.cookies.guest, 'base64').toString();
   	var obj = serialize.unserialize(str);
   	if (obj.username) {
     	res.send("Hello " + escape(obj.username) + ". This page is currently under maintenance for Guest users. Please go back to the login page");
   }
 } else {
	 var username = req.body.username 
	 var country = req.body.country 
	 var city = req.body.city
	 var serialized_info = `{"username":"${username}","country":"${country}","city":"${city}"}`
     var encoded_data = new Buffer(serialized_info).toString('base64');
	 res.cookie('guest', encoded_data, {
       maxAge: 900000,
       httpOnly: true
     });
 }
 res.send("Hello!");
});
app.listen(process.env.PORT || 7777);
console.log("Listening on port 7777...");

