const express = require('express')
const Dockerode = require('dockerode')
const tmp = require('tmp')
const fsO = require('fs')
const fs = require('fs/promises')
const bodyParser = require('body-parser')
const crypto = require('crypto')
const winston = require('winston')
const morgan = require('morgan')
const { verify } = require('hcaptcha')
const app = express()
const port = 3000
const docker = new Dockerode()
require('winston-daily-rotate-file')
const { format, transports } = winston
const { combine, timestamp, label, printf } = format
const devNull = fsO.createWriteStream('/dev/null')

const m = new Map()
const logger = winston.createLogger({
  level: 'info',
  format: combine(
    label({ label: 'right meow!' }),
    timestamp(),
    printf(({ level, message, ip, timestamp }) => {
      return `${timestamp} [${ip}]: ${message}`
    })
  ),
  transports: [
    new transports.DailyRotateFile({
      datePattern: 'YYYY-MM-DD-HH',
      zippedArchive: false,
      maxSize: '20m',
      filename: `${__dirname}/logs/docker/application-%DATE%.txt`
    }),
    new transports.Console()
  ]
})
app.use(bodyParser.json())
app.use(morgan('short'))
app.use(morgan('short', {
  stream: fsO.createWriteStream(`${__dirname}/logs/access.log`, { flags: 'a' })
}))
app.get('/', (req, res) => {
  res.sendFile(`${__dirname}/index.html`)
})

app.post('/build', async (req, res) => {
  const { code } = req.body
  if (typeof code !== 'string') {
    return res.status(400).end()
  }
  const hCaptchaData = await verify(process.env.HCAPTCHA_SECRET, req.body['h-captcha-response'])
  if (hCaptchaData.success !== true) {
    return res.status(403).json({ error: 'Invalid captcha' })
  }
  const log = logger.child({ ip: `${req.ip}` })
  log.info(`Code: ${JSON.stringify(code)}`)
  const id = crypto.randomBytes(16).toString('hex')
  tmp.dir({
    tmpdir: process.env.HOST_TMP_PATH || '/tmp'
  }, async function (err, path, cleanupCallback) {
    log.info(`Temp dir: ${path}`)
    if (err) {
      res.status(500).send(err.message)
    }
    m.set(id, path)
    fs.mkdir(`${path}/src`)
      .then(() => fs.mkdir(`${path}/dist`))
      .then(() => fs.writeFile(`${path}/dist/id`, id, 'utf-8'))
      .then(() => fs.writeFile(`${path}/.prettierrc`, code, 'utf-8'))
      .then(() => fs.chmod(`${path}/dist/id`, '0777'))
      .then(() => fs.chmod(`${path}/dist`, '0777'))
      .then(() => docker.run('prettieronline', [], devNull, {
        Name: id,
        NetworkDisabled: true,
        NetworkMode: 'none',
        HostConfig: {
          Binds: [
            `${path}/.prettierrc:/app/.prettierrc`,
            `${path}/dist:/app/dist/`
          ]
        }
      }))
      .then(data => {
        const container = data[1]
        log.info(`Docker done: ${container.id}`)
        const ret = container.remove()
        if (data[0].StatusCode !== 0) {
          return ret.then(() => Promise.reject(new Error(`Docker failed: Error code ${data[0].StatusCode}`)))
        }
        return ret
      })
      .then(() => Promise.race([
        fs.readFile(`${path}/dist/${id}`, 'utf-8').then(sign => {
          const calculatedSign = crypto.createHash('sha256').update(Buffer.from(id, 'utf-8')).digest().toString('hex')
          if (sign.trim() !== calculatedSign) {
            return Promise.reject(new Error('Sign mismatched'))
          }
          return fs.readFile(`${path}/dist/ret.js`, 'utf-8')
        }).then(file => {
          log.info(`File: ${JSON.stringify(file)}`)
          return res.json({ file })
        }),
        new Promise(resolve => setTimeout(resolve, 10000)).then(a => {
          return Promise.reject(new Error('timeout'))
        })
      ]))
      .catch(e => {
        log.error(`Error: ${e.message}`)
        return res.json({ error: e.message })
      }).finally(() => {
        fs.rm(path, { recursive: true, force: true })
        cleanupCallback()
      })
  })
})

app.listen(port, () => {
  console.log(`PrettierOnline listening on port ${port}`)
})
