const express = require('express')
const logger = require('morgan')
const session = require('express-session')
const { v4 } = require('uuid')

const app = express()
const io = require('socket.io')({
  path: '/api/socket'
})

// simple user database
const users = Object.create(null)

// reserve alice and bob
Object.assign(users, {
  alice: {
    password: process.env.PASSWORD,
    publicKey: null
  },
  bob: {
    password: process.env.PASSWORD,
    publicKey: null
  }
})

const sessionMiddleware = session({
  secret: v4(),
  name: 'sessionId',
  resave: true,
  saveUninitialized: false
})

app.use(logger('dev'))
app.use(express.json())
app.use(sessionMiddleware)

// signup or login
app.post('/api/login', function (req, res, next) {
  // some validations
  for (const [, value] of Object.entries(req.body)) {
    if (typeof value !== typeof '' || !value) throw new Error('must be non empty string')
  }
  const { username, password, publicKey } = req.body
  if (!username.match(/^[a-z0-9]+$/i)) throw new Error('invalid username')
  if (username.length < 3 || username.length > 30) throw new Error('invalid username')
  if (password.length < 3 || password.length > 30) throw new Error('invalid password')

  if (users[username]) {
    // login flow
    if (users[username].password !== password) throw new Error('password does not match')
    users[username].publicKey = publicKey
  } else {
    // signup flow
    users[username] = {
      password: password,
      publicKey: publicKey
    }
  }
  req.session.username = username
  res.send('success')
})

app.get('/api/publicKey', function (req, res, next) {
  res.send(users[req.query.username].publicKey)
})

app.get('/api/users', function (req, res, next) {
  res.json(Object.keys(users))
})

io.use(function (socket, next) {
  sessionMiddleware(socket.request, socket.request.res, next)
})

io.on('connection', function (socket) {
  let room
  socket.on('join', function (body) {
    room = body.room.toString()
    socket.join(room)
  })
  socket.on('message', function (body) {
    if (room) {
      io.to(room).emit('message', {
        ...body,
        id: v4(),
        from: socket.request.session.username
      })
    }
  })
  socket.on('read', function (body) {
    if (room) {
      io.to(room).emit('read', {
        from: socket.request.session.username,
        id: body.id
      })
    }
  })
})

app.use(function (err, req, res, next) {
  res.status(err.status || 500)
  res.send(err.message)
})

module.exports = { app, io }
