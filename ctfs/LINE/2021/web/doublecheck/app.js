const createError = require('http-errors')
const express = require('express')
const bodyParser = require('body-parser')
const path = require('path')
const logger = require('morgan')
const querystring = require('querystring')
const http = require('http')
const process = require('process')

const app = express()
const port = process.env.PORT || '3000'

logger.token('body', (req, res) => req.body.length ? req.body : '-')
app.use(logger(':method :url :status :response-time ms - :res[content-length] :body'))
app.use(bodyParser.text({ type: 'text/plain' }))
app.use(express.static(path.join(__dirname, 'public')))

app.post('/', function (req, res, next) {
  const body = req.body
  if (typeof body !== 'string') return next(createError(400))

  if (validate(body)) return next(createError(403))
  const { p } = querystring.parse(body)
  if (validate(p)) return next(createError(403))

  try {
    http.get(`http://localhost:${port}/api/vote/` + encodeURI(p), r => {
      let chunks = ''
      r.on('data', (chunk) => {
        chunks += chunk
      })
      r.on('end', () => {
        res.send(chunks.toString())
      })
    })
  } catch (error) {
    next(createError(404))
  }
})

const vote = { good: 0, bad: 0 }
app.get('/votes', function (req, res, next) {
  res.json(vote)
})

// internal apis
app.get('/api/vote/:type', internalHandler, function (req, res, next) {
  if (req.params.type === 'bad') vote.bad += 1
  else vote.good += 1
  res.send('ok')
})

app.get('/flag', internalHandler, function (req, res, next) {
  const flag = process.env.FLAG || 'LINECTF{****}'
  res.send(flag)
})

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404))
})

// error handler
app.use(function (err, req, res, next) {
  res.status(err.status || 500)
  res.send(err.message)
})

function internalHandler (req, res, next) {
  if (req.ip === '::ffff:127.0.0.1') next()
  else next(createError(403))
}

function validate (str) {
  return str.indexOf('.') > -1 || str.indexOf('%2e') > -1 || str.indexOf('%2E') > -1
}

module.exports = app
