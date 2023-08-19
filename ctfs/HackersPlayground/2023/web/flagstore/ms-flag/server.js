const express = require('express')
const createError = require('http-errors');

const MS_PORT = 3003
const MS_PRIVATE_PORT = 4003

const flags = require('./flags.json')
const secret = {}
const id_regex = /^[a-zA-Z]+$/

function build_app(){
  const app = express()
  app.use((req, res, next) => {
    console.log(req.url)
    next()
  })
  app.use(express.json())
  return app
}

function handle_error(app){
  app.use(function (req, res, next) {
    next(createError(404));
  })

  app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    if (res.statusCode >= 500) {
      res.json({ message: err.message });
      // res.json({ message: 'Internal server error' });
    } else {
      res.json({ message: err.message });
    }
  })
}


function install_private_handler(app){
}

function install_public_handler(app){
  app.get('/flag/healthcheck', function (req, res) {
    res.status(200).json({ flags: flags.length, })
  })

  // credential
  app.use((req, res, next) => {
    req.credential = {}
    if (req.headers['x-credential']) {
      try{
        req.credential = JSON.parse(atob(req.headers['x-credential']))
        next()
      }catch(_){
      }
    }
    req.status(400).json({ error: 'credential not found' })
  })


}


function init() {
  flags = {}
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