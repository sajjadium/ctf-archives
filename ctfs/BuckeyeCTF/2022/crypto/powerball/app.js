import express from 'express'
import http from 'http'
import { Server } from 'socket.io'
import crypto from 'crypto'

function nextRandomNumber () {
  return (multiplier * seed) % modulus
}

function areArraysEqual (a, b) {
  return (
    a.length === b.length &&
    a.every((x, i) => {
      return x === b[i]
    })
  )
}

function seedToBalls (n) {
  const balls = []
  for (let i = 0; i < 10; i++) {
    balls.push(Number(n % 100n))
    n = n / 100n
  }
  return balls
}

const app = express()
app.use(express.static('static'))

const server = http.createServer(app)
const io = new Server(server)

const modulus = crypto.generatePrimeSync(128, { safe: true, bigint: true })
const multiplier = (2n ** 127n) - 1n
let seed = 2n
for (let i = 0; i < 1024; i++) {
  seed = nextRandomNumber()
}
let winningBalls = seedToBalls(seed)
let lastLotteryTime = Date.now()

setInterval(() => {
  seed = nextRandomNumber()
  winningBalls = seedToBalls(seed)
  lastLotteryTime = Date.now()
}, 60 * 1000)

io.on('connection', (socket) => {
  socket.ticket = { balls: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], submissionTime: 0 }

  socket.on('updateRequest', () => {
    let flag = ''
    if (
      areArraysEqual(socket.ticket.balls, winningBalls) &&
      socket.ticket.submissionTime < lastLotteryTime
    ) {
      flag = process.env.FLAG
    }

    socket.emit('update', {
      last_winning_seed: seed.toString(),
      flag: flag
    })
  })

  socket.on('submitBalls', (balls) => {
    if (!(Array.isArray(balls) && balls.length === 10)) return
    for (let i = 0; i < 10; i++) {
      if (typeof balls[i] !== 'number') return
    }

    socket.ticket = { balls: balls, submissionTime: Date.now() }
  })
})

server.listen(3000, () => {
  console.log('Ready')
})
