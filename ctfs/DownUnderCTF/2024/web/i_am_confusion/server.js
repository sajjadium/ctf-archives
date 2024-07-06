// essentials
const express = require('express')
const app = express()
const jwt = require('jsonwebtoken')
const cookieParser = require('cookie-parser')
var fs = require('fs')
const path = require('path')
const https = require('https')

// ascii art
const asciiArt = fs.readFileSync('ascii-art.txt', 'utf8');

// algs
const verifyAlg = { algorithms: ['HS256','RS256'] }
const signAlg = { algorithm:'RS256' }

// keys
// change these back once confirmed working
const privateKey = fs.readFileSync('keys/priv.key')
const publicKey = fs.readFileSync('keys/pubkeyrsa.pem')
const certificate = fs.readFileSync('keys/fullchain.pem')

// middleware
app.use(express.static(__dirname + '/public'));
app.use(express.urlencoded({extended:false}))
app.use(cookieParser())

app.get('/', (req, res) => {
  res.status(302).redirect('/login.html')
});

app.post('/login', (req,res) => {
  var username = req.body.username
  var password = req.body.password

  if (/^admin$/i.test(username)) {
    res.status(400).send("Username taken");
    return;
  }

  if (username && password){
    var payload = { user: username };
    var cookie_expiry =  { maxAge: 900000, httpOnly: true }

    const jwt_token = jwt.sign(payload, privateKey, signAlg)

    res.cookie('auth', jwt_token, cookie_expiry)
    res.redirect(302, '/public.html')
  } else {
    res.status(404).send("404 uh oh")
  }
});

app.get('/admin.html', (req, res) => {
  var cookie = req.cookies;
  jwt.verify(cookie['auth'], publicKey, verifyAlg, (err, decoded_jwt) => {
    if (err) {
      res.status(403).send("403 -.-");
    } else if (decoded_jwt['user'] == 'admin') {
      res.sendFile(path.join(__dirname, 'admin.html')) // flag!
    } else {
      res.status(403).sendFile(path.join(__dirname, '/public/hehe.html'))
    }
  })
})

app.get('/public.html', (req, res) => {
  var cookie = req.cookies;
  jwt.verify(cookie['auth'], publicKey, verifyAlg, (err, decoded_jwt) => {
    if (err) {
      res.status(302).redirect('/login.html');
    } else if (decoded_jwt['user']) {
      res.sendFile(path.join(__dirname, 'public.html'))
    }
  })
})


const credentials = {key: privateKey, cert: certificate}
const httpsServer = https.createServer(credentials, app)
const PORT = 1337;

httpsServer.listen(PORT, ()=> {
  console.log(`HTTPS Server running on port ${PORT}`);
})
