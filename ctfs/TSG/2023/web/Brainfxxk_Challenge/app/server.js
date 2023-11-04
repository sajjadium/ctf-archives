import express from 'express'
import { createClient } from 'redis'

function asyncRoute(fn) {
    return (req, res, next) => {
        return fn(req, res, next).catch(next)
    }
}

const redisClient = createClient({
    url: process.env.REDIS_URL
})
redisClient.on('error', err => console.log('Redis Client Error', err))
await redisClient.connect()

const redisReporterClient = createClient({
    url: process.env.REDIS_REPORTER_URL
})
redisReporterClient.on('error', err => console.log('Redis Client Error', err))
await redisReporterClient.connect()

const app = express()

app.set('view engine', 'ejs')

app.use(express.static('public'))
app.use(express.urlencoded({ extended: false }))

app.use((req, res, next) => {
    const cssFiles = ['https://unpkg.com/sakura.css@1.4.1/css/sakura.css']
    res.setHeader('Content-Security-Policy', `style-src 'self' ${cssFiles.join(' ')} ; script-src 'self' ; object-src 'none' ; font-src 'none'`)
    next()
})

app.get('/', (_req, res) => {
    res.render('index')
})

app.post('/submit', (req, res) => {
    const code = req.body.code
    if (!code) {
        res.send('Please submit a code')
        return
    }
    const codeId = [...Array(16)].map(e=>Math.floor(Math.random() * 36).toString(36)).join('')
    redisClient.set(codeId, code)
    res.redirect(`/${codeId}`)
})

app.post('/report', asyncRoute(async (req, res) => {
    const targetPath = req.body.path
    if (!targetPath) {
        res.send('Please specify page path')
        return
    }

    await redisReporterClient.rPush('query', targetPath)
    await redisReporterClient.incr('queued_count')
    res.send('Reported. Admin will check the page.')
}))

app.get('/minify', (req, res) => {
    const code = req.query.code ?? ''
    res.send(code.replaceAll(/[^><+\-=r\[\]]/g, ''))
})

app.get('/:codeId', asyncRoute(async (req, res) => {
    const code = await redisClient.get(req.params.codeId)
    if (!code) {
        res.status(404).send('Not found')
        return
    }
    res.render('show', {
        code,
        pagePath: req.originalUrl
    })
}))

app.listen(37291)
