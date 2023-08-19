const express = require('express')
const jwt = require('jsonwebtoken');
const createError = require('http-errors');

const ADMIN_PASSWD = process.env.ADMIN_PASSWD || 'ADMIN_PASSWD'
const MS_PORT = 3001
const MS_PRIVATE_PORT = 4001

let users = {}
const secret = {}
const id_regex = /^[a-zA-Z]+$/

function build_app(){
  const app = express()
  app.use(express.json())
  return app
}

function handle_error(app){
  app.use(function (req, res, next) {
    next(createError(404))
  })

  app.use(function (err, req, res, next) {
    res.status(err.status || 500)
    if (res.statusCode >= 500) {
      res.json({ message: err.message })
    } else {
      res.json({ message: err.message })
    }
  })
}


function install_private_handler(app){
  app.post('/_user/jwt', function (req, res) {
    let jwt_parsed = jwt.verify(req.body.jwt, secret.keys.JWT_SECRET_KEY)
    let user = {}
    if (jwt_parsed && jwt_parsed.id) {
      user = { ...jwt_parsed }
    }
    res.json(user)
  })
}

function install_public_handler(app){
  app.post('/user/signin', function (req, res) {
    if (!(req.body.hasOwnProperty('id') && req.body.hasOwnProperty('passwd'))) {
      res.status(400).json({ error: 'require params id, passwd' })
      return
    }

    const { id, passwd } = req.body

    if (!users.hasOwnProperty(id)) {
      res.status(400).json({ error: 'invalid id & passwd' })
      return
    }

    if (users[id].passwd !== passwd) {
      res.status(400).json({ error: 'invalid id & passwd' })
      return
    }

    const user = users[id]
    const token = jwt.sign({ id: user.id, name: user.name }, secret.keys.JWT_SECRET_KEY);

    res.status(200).cookie('jwt', token, {
      expires: new Date(Date.now() + 8 * 3600000)
    }).json({ id: user.id })
  })

  app.post('/user/signup', function (req, res) {
    if (!(req.body.hasOwnProperty('id') && req.body.hasOwnProperty('passwd'))) {
      res.status(400).json({ error: 'require params id, passwd' })
      return
    }
    const { id, passwd, name, email } = req.body
    if (!id_regex.test(id)) {
      res.status(400).json({ error: 'id should be alphabet' })
      return
    }

    if (users.hasOwnProperty(id)) {
      res.status(400).json({ error: 'id exists' })
      return
    }

    if (Object.keys(users).length > 20000) {
      init()
    }
    users[id] = { id, passwd, name, email }
    res.status(201).json({ id })
  })

  // credential
  app.use((req, res, next) => {
    req.credential = {}
    if (req.headers['x-credential']) {
      try{
        req.credential = JSON.parse(atob(req.headers['x-credential']))
        return next()
      }catch(_){
      }
    }
    res.status(400).json({ error: 'credential not found' })
  })

  app.get('/user/me', function (req, res) {
    if (req.credential.id)
      res.status(200).json(req.credential)
    else
      res.status(401).json({error:'unauthorized'})
  })
}


function init() {
  users = {}
  users.admin = { id: 'admin', passwd: ADMIN_PASSWD }
}

async function get_secrets() {
  while(true){
    try {
      const res = await fetch('http://msproxy/_secret/keys')
      const data = await res.json()
      return { ...data.keys }
    } catch(e) {
      await new Promise(r => setTimeout(() => r, 1000))
    }
  }
}

async function main() {
  init()
  secret.keys = await get_secrets()
  try {
    const public_app = build_app()
    install_public_handler(public_app)
    handle_error(public_app)
    public_app.listen(MS_PORT)
  } catch (e){
    console.error(e)
  }

  const priv_app = build_app()
  install_private_handler(priv_app)
  handle_error(priv_app)
  priv_app.listen(MS_PRIVATE_PORT)

}
main()