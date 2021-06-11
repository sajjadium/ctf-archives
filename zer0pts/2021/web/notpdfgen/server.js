const express = require('express')
const PDFDocument = require('pdfkit');
const bodyParser = require("body-parser");
const fs = require('fs');
const uuid = require('uuid')
var morgan = require('morgan')
var path = require('path')
var redis = require('redis')
var request = require('request');
var https = require('https');


const app = express()

var accessLogStream = fs.createWriteStream(path.join(__dirname, 'access.log'), { flags: 'a' })
app.use(morgan('combined', { stream: accessLogStream }))

app.use('/static', express.static('public'))
app.use(function(req, res, next) {
  res.header('Cross-Origin-Opener-Policy', 'unsafe-none');
  next();
});

app.use("/uploads/:file",function(req, res, next){
	if(req.headers['sec-fetch-dest']=='embed'){
		next();
	}
	else{
		res.send('sorry');
	}
});

app.use("/9ab76d233b52165bf9450f81d0784425",function(req, res, next){
	if(req.headers['sec-fetch-dest']=='embed'){
		next();
	}
	else{
		res.send('sorry');
	}
});



app.get('/9ab76d233b52165bf9450f81d0784425',(req,res) => {
  const ip = req.connection.remoteAddress;
  var filename = './9ab76d233b52165bf9450f81d0784425'
  if(ip === "127.0.0.1"  || ip === "10.5.0.3"  || ip === "::ffff:10.5.0.3" || ip === "::1" || ip === "::ffff:127.0.0.1"){
    if(fs.existsSync(filename)){
      var file = fs.createReadStream(filename);
      file.pipe(res);
    }else{
      res.send('contact admin');
    }
  }
});

app.get("/adminFlag", (req, res) => {
  var filename = '/9ab76d233b52165bf9450f81d0784425'
  res.send(`<!Doctype html>
  <head>
  <title>title</title>
  <script src="/static/bundle.js"></script>
  </head>
  <div id="app">
    <h3>{{title}}</h3>
  </div>
  <embed src="${filename}" type="application/pdf" style="width:100%;height:70vh;"></embed>
    <p id="name"></p>
    <p> One more conversion? </p>
    <form action="/text" method="get" >
      <input id="text" type="input" name="text"/><br>
      <input type="submit"/>
    </form>

    <a href="/report">report?</a>
  <html>

  <script>
  var params = parseQuery(location.search.slice(1));
  var app = new Vue({
      el: '#app',
      data: {
          title: 'Here is your pdf'
      }
  });
  if(params.name && params.text ){
    document.getElementById("name").innerText = "Hi, "+ params.name;
    document.getElementById("text").value = params.text;
  }
  </script>
  `);
});



var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.get('/', (req, res) => {
  res.send(`<!Doctype html>
  <head>
  <title>title</title>
  <script src="/static/bundle.js"></script>
  </head>

  <div id="app">
    <h3>{{title}}</h3>
  </div>
    <p id="name"></p>
    <form action="/text" method="get" >
      <input id="text" type="input" name="text"/><br>
      <input type="submit"/>
    </form>
  <script>
  var params = parseQuery(location.search.slice(1));
  var app = new Vue({
      el: '#app',
      data: {
          title: 'Text to PDF Convertor'
      }
  });
  if(params.name && params.text ){
    document.getElementById("name").innerText = "Hi, "+ params.name;
    document.getElementById("text").value = params.text;
  }
  </script>
  `)
});

app.get("/uploads/:file", (req, res) => {
  var userPath = req.params.file;
  var sanitizedPath = userPath.replace(/[^a-f0-9-]/gi,'_')
  var filename = './uploads/' + sanitizedPath;
  if(fs.existsSync(filename)){
    var file = fs.createReadStream(filename);
    file.on('end', function(){
      fs.unlink(filename, function(err){
        if(err){
          console.log(err);
        }
      });
    })
    file.pipe(res);
  }else{
    res.send('oh its deleted');
  }
});

app.get('/text', urlencodedParser, (req, res) => {
  const ip = req.connection.remoteAddress
  console.log(ip);
  let pdfDoc = new PDFDocument;
  var filename = './uploads/' + uuid.v4()
  pdfDoc.pipe(fs.createWriteStream(filename));
  console.log(ip)
  pdfDoc.text(req.query.text);
  pdfDoc.end();
  res.send(`<!Doctype html>
  <head>
  <title>title</title>
  <script src="/static/bundle.js"></script>
  </head>
  <div id="app">
    <h3>{{title}}</h3>
  </div>
  <embed src="${filename}" type="application/pdf" style="width:100%;height:70vh;"></embed>
    <p id="name"></p>
    <p> One more conversion? </p>
    <form action="/text" method="get" >
      <input id="text" type="input" name="text"/><br>
      <input type="submit"/>
    </form>

    <a href="/report">report?</a>
  <html>

  <script>
  var params = parseQuery(location.search.slice(1));
  var app = new Vue({
      el: '#app',
      data: {
          title: 'Here is your pdf'
      }
  });
  if(params.name && params.text ){
    document.getElementById("name").innerText = "Hi, "+ params.name;
    document.getElementById("text").value = params.text;
  }
  </script>
  `);
});

app.get('/report', (req, res) => {
  res.send(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Report</title>
  </head>
  <body>
    <form action="/report" method="post">
      <input type="text" name="url">
      <input type="hidden" id="g-recaptcha-response" name="g-recaptcha-response">
      <input type="submit" value="report">
    </form>
  </body>
  <script src="https://www.google.com/recaptcha/api.js?render=6Lf-omgaAAAAAIDCKcZi3VL3gJTatL7BSlzxBcq0"></script>
  <script>
  grecaptcha.ready(function() {
        grecaptcha.execute('6Lf-omgaAAAAAIDCKcZi3VL3gJTatL7BSlzxBcq0', {action:'validate_captcha'})
                  .then(function(token) {
            document.getElementById('g-recaptcha-response').value = token;
        });
    });
  </script>
</html>

  `)
});

app.post('/report', urlencodedParser,(req, res) => {
  var url = req.body.url;
  if(req.body['g-recaptcha-response'] === undefined || req.body['g-recaptcha-response'] === '' || req.body['g-recaptcha-response'] === null)
  {
    return res.send("captcha verification failed");
  }
  const secretKey = "(redacted)";
  const verificationURL = "https://www.google.com/recaptcha/api/siteverify?secret=" + secretKey + "&response=" + req.body['g-recaptcha-response'] + "&remoteip=" + req.connection.remoteAddress;

  request(verificationURL,function(error,response,body) {
    body = JSON.parse(body);
    if(body.success !== undefined && !body.success) {
      return res.send("captcha verification failed");
    }
    else{
      const client = redis.createClient({
        host: 'redis1',
        port: 6379
      });
      client.rpush('url',url)
      client.on('error', err => {
        console.log('Error redis: ' + err);
      });
      res.send('reported');
    }
  });
});

module.exports = app