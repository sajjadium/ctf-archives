const express = require('express')

const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY || 'JWT_SECRET_KEY'
const MS_PORT = 3002
const MS_PRIVATE_PORT = 4002

function build_app(){
  const app = express()
  return app
}

function handle_error(app){
  app.use(function(req, res, next) {
    res.status(404);
    res.json({ error: 'Not found' });
  })
}


function run_public_server(){
  const app = build_app()

  app.get('/secret/health_check', function (req, res) {
    res.json('ok')
  })

  handle_error(app)
  app.listen(MS_PORT)
}

function run_private_server(){
  const app = build_app()

  app.get('/_secret/keys', function (req, res) {
    res.json({ keys: { JWT_SECRET_KEY } })
  })

  handle_error(app)
  app.listen(MS_PRIVATE_PORT)
}

run_public_server()
run_private_server()