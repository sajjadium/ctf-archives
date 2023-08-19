const express = require('express')
const createError = require('http-errors');
const crypto = require('crypto');

const FLAG = process.env.FLAG || 'sctf{FAKE_FLAG}'
const MS_PORT = 3004
const MS_PRIVATE_PORT = 4004

let orders = {}

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
}

function install_public_handler(app){
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

  app.get('/order/orders', function (req, res) {
    const { id } = req.credential
    if (!id) {
      res.status(401).json({error:'unauthorized'})
      return
    }

    if (!orders.hasOwnProperty(id)){
      res.status(200).json([])
      return
    }

    res.status(200).json(Object.values(orders[id]))
  })

  app.get('/order/orders/:orderid', function (req, res) {
    const { id } = req.credential
    if (!id) {
      res.status(401).json({error:'unauthorized'})
      return
    }

    res.status(200).json(orders[id][req.params.orderid])
  })

  app.post('/order/orders', function (req, res) {
    const { id } = req.credential
    if (!id) {
      res.status(401).json({error:'unauthorized'})
      return
    }

    const { flag } = req.body
    const uuid = crypto.randomUUID()

    if(!orders.hasOwnProperty(id)){
      orders[id] = {}
    }

    orders[id][uuid] = { ...flag, id:uuid, created:(new Date()).getTime() }

    res.status(200).json(orders[id][uuid])
  })

}

function init() {
  const uuid = crypto.randomUUID()
  orders.admin = {}
  orders.admin[uuid] = {
    id: uuid,
    "flag":"🏁",
    "name": "Admin Flag",
    "content": FLAG,
    "level": 1,
  }
}

async function main() {
  init()

  const public_app = build_app()
  install_public_handler(public_app)
  handle_error(public_app)
  public_app.listen(MS_PORT)

  const priv_app = build_app()
  install_private_handler(priv_app)
  handle_error(priv_app)
  priv_app.listen(MS_PRIVATE_PORT)

}
main()