import express from 'express'
import sqlite3 from 'sqlite3'
import { open } from 'sqlite'

const app = express()
let db = null

app.use(express.static('static'))
app.set('view engine', 'ejs')

function internal (req, res, next) {
  if (
    req.socket.remoteAddress === '172.16.0.11' ||
    req.socket.remoteAddress === '::ffff:172.16.0.11'
  ) {
    return next()
  }

  return res.status(403).end()
}

async function getData (user) {
  return await db.get(
    'SELECT balance, avatar FROM account WHERE user = ?',
    user
  )
}

async function setBalance (user, balance) {
  return await db.run(
    'UPDATE account SET balance = ? WHERE user = ?',
    balance,
    user
  )
}

app.get('/add_user', internal, async (req, res) => {
  const user = req.query.user
  if (user === undefined || user.length > 64) {
    return res.status(400).json({ error: 'Invalid user string' })
  }

  const avatar = req.query.avatar || '/avatar.png'

  await db.run(
    'INSERT OR IGNORE INTO account (user, avatar) VALUES (?, ?)',
    user,
    avatar
  )
  return res.status(200).end()
})

app.get('/balance', async (req, res) => {
  const user = req.query.user
  if (user === undefined || user.length > 64) {
    return res.status(400).json({ error: 'Invalid user string' })
  }

  const data = await getData(user)
  if (data === undefined) {
    return res.status(404).json({ error: 'Invalid user' })
  }

  return res.json(data.balance)
})

app.get('/set_balance', internal, async (req, res) => {
  const user = req.query.user
  if (user === undefined || user.length > 64) {
    return res.status(400).json({ error: 'Invalid user string' })
  }

  const balance = parseInt(req.query.balance)
  if (isNaN(balance)) {
    return res.status(400).json({ error: 'Invalid balance' })
  }

  await setBalance(user, balance)
  return res.status(200).end()
})

app.get('/rich', async (_req, res) => {
  const ans = await db.all(
    'SELECT user, balance FROM account ORDER BY balance DESC LIMIT 10'
  )
  return res.json(ans)
})

app.get('/', (_req, res) => {
  res.render('pages/index')
})

app.get('/badge', async (req, res) => {
  const user = req.query.user
  if (user === undefined || user.length > 64) {
    return res.status(400).json({ error: 'Invalid user string' })
  }

  const data = await getData(user)
  if (data === undefined) {
    return res.status(404).json({ error: 'Invalid user' })
  }

  const balance = data.balance
  const avatar = data.avatar
  const css = (req.query.css || '').replace(/</g, '&lt;').replace(/>/g, '&gt;')

  let bg = 0
  if (balance >= 750) bg = 3
  else if (balance >= 500) bg = 2
  else if (balance >= 250) bg = 1
  bg = `/bg${bg}.png`

  res.render('pages/badge', { user, balance, avatar, bg, css })
})

app.listen(3000, async () => {
  db = await open({ filename: ':memory:', driver: sqlite3.Database })
  await db.run(`CREATE TABLE account (
  user TEXT NOT NULL,
  balance INTEGER DEFAULT 0,
  avatar TEXT NOT NULL,
  PRIMARY KEY(user)
);`)
  await db.run(
    'INSERT INTO account (user, avatar) VALUES ("nobody#0000", "/avatar.png");'
  )

  console.log('Listening ...')
})
