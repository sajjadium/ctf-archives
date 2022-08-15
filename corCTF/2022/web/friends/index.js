const crypto = require('crypto')
const express = require('express')
const app = express()

app.use(require('cookie-parser')())
app.use(require('body-parser').urlencoded({ extended: false }))

// map of username -> password
const users = new Map()
// map of token -> username
const sessions = new Map()
// map of username -> [username]
const followers = new Map()
// map of username -> username -> { r: relationship, n: note }
const following = new Map()

// sanitize text
const sanitize = (text) => (
  (text ?? '')
    .toString()
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
)

app.use('/', (req, _res, next) => {
  // no cookie
  if (!req.cookies.token) {
    return next()
  }

  // invalid token
  if (!sessions.has(req.cookies.token)) {
    return next()
  }

  // otherwise, they are logged in
  req.username = sessions.get(req.cookies.token)
  next()
})

app.get('/', (req, res) => {
  // if logged in already
  if (req.username) {
    return res.redirect('/user')
  }

  // otherwise...
  res.send(`
    <strong>log in or register</strong>
    <form method="post" action="/login">
      <input type="text" name="u" placeholder="username"><br>
      <input type="text" name="p" placeholder="password"><br>
      <input type="text" name="c" placeholder="confirm password"><br>
      <input type="submit" value="login">
    </form>
    <em>${sanitize(req.query.m)}</em>
  `)
})

app.get('/user', (req, res) => {
  // if not logged in
  if (!req.username) {
    return res.redirect('/')
  }

  // get followers
  const mine = followers
    .get(req.username)
    .filter(v => v !== undefined)

  if (mine.includes('admin')) {
    // lock the account so people don't stumble onto the flag
    users.set(req.username, crypto.randomBytes(16).toString('hex'))

    // give the flag
    return res.send(
      `Endorsed by the admin?! Here's your flag: ${process.env.FLAG}`
    )
  }

  res.send(`
    <strong>home page: ${sanitize(req.username)}</strong>
    <hr>
    <strong>follow user</strong>
    <form method="post" action="/follow">
      <input type="text" name="u" placeholder="username"><br>
      <input type="text" name="r" placeholder="relationship"><br>
      <input type="text" name="n" placeholder="note"><br>
      <input type="submit" value="follow">
    </form>
    <strong>unfollow user</strong>
    <form method="post" action="/remove">
      <input type="text" name="u" placeholder="username"><br>
      <input type="submit" value="unfollow">
    </form>
    <em>${sanitize(req.query.m)}</em>
    <hr>
    <strong>following:</strong>
    <ul>
      ${
        [...following.get(req.username).entries()]
          .map(([ user, { r, n } ]) => {
            return (
              `<li>${sanitize(user)}: ${sanitize(r)} (${sanitize(n)})</li>`
            )
          })
          .join('\n')
      }
    </ul>
    <hr>
    <strong>followers:</strong>
    <ul>
      ${mine.map(v => `<li>${sanitize(v)}</li>`).join('\n')}
    </ul>
    <hr>
  `)
})

app.post('/login', (req, res) => {
  const body = req.body
  const params = ['u', 'p', 'c']

  // if already logged in, then no need
  if (req.username) {
    return res.redirect('/user')
  }

  // force all params to be strings for safety
  [body.u, body.p, body.c] = params.map(
    p => (body[p] ?? '').toString()
  )

  // make sure usernames are long (prevent login guessing)
  if (body.u.length < 8) {
    return res.redirect('/?m=username+too+short')
  }

  if (body.p !== body.c) {
    return res.redirect('/?m=passwords+do+not+match')
  }

  const token = crypto.randomBytes(16).toString('hex')

  // handle the existing user case
  if (users.has(req.body.u)) {
    const user = users.get(req.body.u)

    // if password is incorrect
    if (user !== req.body.p) {
      return res.redirect('/?m=user+exists;+incorrect+password')
    }
  }

  // otherwise, create a new user
  users.set(req.body.u, req.body.p)

  // create the empty followers list
  if (!followers.has(req.body.u)) {
    followers.set(req.body.u, [])
  }

  // create the empty following map
  if (!following.has(req.body.u)) {
    following.set(req.body.u, new Map())
  }

  // on successful login or registration
  sessions.set(token, req.body.u)
  res.cookie('token', token)
  res.redirect('/user')
})

app.post('/follow', (req, res) => {
  if (!req.username) {
    return res.redirect('/?m=must+be+logged+in+to+add+follower')
  }

  const body = req.body
  const params = ['u', 'r', 'n']
  const mine = followers.get(req.username)

  // force all params to be strings for safety
  [body.u, body.r, body.n] = params.map(
    p => (body[p] ?? '').toString()
  )

  // if the user is trying to add themselves
  if (req.username === body.u) {
    return res.redirect('/user?m=cannot+add+yourself')
  }

  // if the user doesn't exist
  if (!users.has(body.u)) {
    return res.redirect('/user?m=user+does+not+exist')
  }

  const theirs = followers.get(body.u)
  // if a follower exists already
  if (theirs.some(c => c.u === req.username)) {
    return res.redirect('/user?m=already+following')
  }

  // ignore deleted entries when calculating friends
  const friends = (
    mine.filter(v => v !== undefined).length +
    following.get(req.username).size
  )

  // stop people from using too much memory
  if (friends > 1000) {
    return res.redirect('/user?m=reached+max+friends')
  }

  // otherwise, add the follower onto their list
  theirs.push(req.username)
  following.get(req.username).set(body.u, { r: body.r, n: body.n })

  res.redirect('/user?m=followed!')
})

app.post('/remove', (req, res) => {
  if (!req.username) {
    return res.redirect('/?m=must+be+logged+in+to+remove+follower')
  }

  // make sure the param is a string
  const user = (req.body.u ?? '').toString()

  // make sure the user exists
  if (!users.has(user)) {
    return res.redirect('/user?m=user+does+not+exist')
  }

  // delete is convenient and safe for -1 index
  // no check needed
  const theirs = followers.get(user)
  delete theirs[theirs.indexOf(req.username)]

  // remove from the following map
  following.get(req.username).delete(user)

  res.redirect('/user?m=unfollowed!')
})

app.listen(3000, () => console.log('listening'))
