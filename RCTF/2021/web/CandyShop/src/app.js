const path = require('path')

const crypto = require('crypto')
const express = require('express')
const pug = require('pug')
const bodyPaser = require('body-parser')
const cookiePaser = require('cookie-parser')

const indexRouter = require('./routes/index')

const app = express()
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')

app.use('/static', express.static(path.join(__dirname, 'static')))
app.use(cookiePaser(crypto.randomBytes(32).toString()))
app.use(bodyPaser.urlencoded())

app.use('/', indexRouter)

process.on('uncaughtException', function (err) {
    console.log(err);
});

app.listen(3000,'0.0.0.0', () => {
    console.log('app start listen at http://localhost:3000')
})