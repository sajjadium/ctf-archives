const express = require('express')
const { createProxyMiddleware } = require('http-proxy-middleware')
const createError = require('http-errors')

const app = express()
const yaml = require('js-yaml');
const fs = require('node:fs');
const cookie_parser = require('cookie-parser')
const jwt = require('jsonwebtoken');
const fetch = require('node-fetch').default;


const config = yaml.load(fs.readFileSync('config.yml', 'utf8'));


app.use(cookie_parser())

// auth filter
app.use(async (req, res, next) => {
  req.headers['x-credential'] = btoa(JSON.stringify({}))
  if (req.cookies.jwt) {
    try {
      const user = jwt.verify(req.cookies.jwt, secret.keys.JWT_SECRET_KEY)
      if (user && user.id) {
        req.headers['x-credential'] = btoa(JSON.stringify(user))
      }
    }catch(e){
      // ignore
    }
  }
  next()
})

const gateways = {}
const proxy = createProxyMiddleware({
  target: `http://msproxy`,
  pathRewrite: (path, req) => {
    return encodeURI(`/${req.params.ms}/${req.params[0]}`) /* rest of path */
  }
})

app.all('/api/:ms/*', (req, res, next) => {
  if (gateways.hasOwnProperty(req.params.ms)) {
    proxy(req, res, next)
  } else {
    res.status(404).json({error: 'Not found'})
  }
})



app.use(function (req, res, next) {
  next(createError(404));
})

app.use(function (err, req, res, next) {
  res.status(err.status || 500);
  res.json({ message: err.message });
})


function load_gateway_config() {
  for (const ms in config.gateway.proxy) {
    const ms_config = config.gateway.proxy[ms]
    gateways[ms] = { ...ms_config }
  }
}

const secret = {}

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
  secret.keys = await get_secrets()
  load_gateway_config()
  app.listen(3000)
}
main()

