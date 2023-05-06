const express = require('express');
var engines = require('consolidate');
const bodyParser = require('body-parser');

const app = express();

app.engine('html', engines.mustache);
app.set('view engine', 'html');
app.set('views', __dirname + '/views');
app.use(express.static('static'));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function(req, res){
	return res.render('index', {});
})

app.post('/', function(req, res){
	const regex = /[a-zA-Z]/g;
	var width = req.body.width;
	var height = req.body.height;
	if(width === '' || height === ''){
		return res.render('index', {'error':'one of the field is empty...'});
	}
	if(width.length > 10 || height.length > 10){
		return res.render('index', {'error':'width or height are too large !'});
	}
	return res.render('index', {'result':'Result: ' + eval('(' + width + '**2 + ' + height + '**2) ** (1/2);')});
})

app.listen(3001)
