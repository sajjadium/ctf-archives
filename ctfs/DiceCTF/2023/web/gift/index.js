const crypto = require('crypto')
const fs = require('fs')

const logger = (data) => fs.appendFile('debug', data, () => {})

const express = require('express')
const app = express()

app.use(express.static('static'))

app.use('*', (req, _res, next) => {
    req.token = req.headers['cookie']?.split('; ')[0]?.split('=')[1]
    req.user = users.get(req.token)
    next()
})

app.post('/api/*', async (req, _res, next) => {
    const data = []
    req.on('data', [].push.bind(data))
    await new Promise((res) => req.on('end', res))
    try {
        req.body = JSON.parse(Buffer.concat(data).toString())
    } catch {
        req.body = {}
    }
    next()
})

const users = new Map()
const gifts = new Map()
const names = new Set()

const createHex = () => crypto.randomBytes(16).toString('hex')

const createUser = (name, balance) => {
    const id = createHex()
    name = (name ?? '').toString()
    if (name === '') { return void 0 }
    if (names.has(name)) { return void 1 }

    // name is valid and not taken, so create the user
    [console.log, logger]?.[process.env.LOG]?.('created user')

    users.set(id, { name, balance })
    names.add(name)
    return id
}

const createGift = (userToken, amount) => {
    const public = createHex()
    const private = createHex()

    if (!users.has(userToken)) { return void 0 }
    if (amount < 0) { return void 1 }
    if (isNaN(amount)) { return void 2 }

    const data = {}

    // user associated with gift
    data.user = userToken
    // gift amount
    data.amount = amount
    // token for modifying gift data
    data.private = private
    // default gift usage limit of 0
    data.limit = 0

    // token is correct and amount is positive, so create the gift
    [console.log, logger]?.[process.env.LOG]?.('created gift')

    gifts.set(public, data)

    return { public, private }
}

app.post('/api/login', (req, res) => {
    const balance = req.body.admin === process.env.ADMIN ? Infinity : 100
    const id = createUser(req.body.name, balance)
    if (id) {
        res.set('set-cookie', `token=${id}; path=/; max-age=31536000`)
        return res.json({ id })
    }
    res.status(400).json({ error: 'invalid name' })
})

app.get('/api/info', (req, res) => {
    if (req.user) { return res.json(req.user) }
    res.status(401).json({ error: 'not logged in' })
})

app.post('/api/config/:public', (req, res) => {
    const gift = gifts.get(req.params.public)
    if (!gift) { return res.status(404).json({ error: 'not found' }) }
    if (gift.private !== req.body.private) {
        return res.status(401).json({ error: 'unauthorized' })
    }

    const limit = +req.body.limit
    if (limit < 0) { return res.status(400).json({ error: 'invalid limit' }) }

    // limit is valid
    [console.log, logger]?.[process.env.LOG]?.('set gift limit')

    gift.limit = limit

    res.json({})
})

const render = async (file, data) => {
    const filename = `views/${file}.html`
    const content = await fs.promises.readFile(filename, 'utf8')
    return data
        ? content.replace(
            '<data>',
            JSON.stringify(data).replaceAll('"', '&quot;')
        )
        : content
}

app.get('/login', async (req, res) => {
    if (req.user) { return res.redirect('/') }
    res.send(await render('login'))
})

app.get('/logout', async (_req, res) => {
    res.set('set-cookie', `token=; path=/; max-age=0`)
    res.redirect('/login')
})

app.get('*', (req, res, next) => {
    res.set(
        'content-security-policy', [
            'connect-src \'self\'',
            'default-src \'none\'',
            'style-src \'self\'',
            'script-src \'self\'',
        ].join('; ')
    )
    if (!req.user) { return res.redirect('/login') }
    next()
})

app.get('/', async (_req, res) => {
    res.send(await render('index'))
})

app.get('/create/:amount', async (req, res) => {
    const data = createGift(req.token, +req.params.amount)
    res.send(await render('create', data ?? { error: 'failed' }))
})

app.get('/claim/:public', (req, res) => {
    const gift = gifts.get(req.params.public)

    if (!gift) { return res.redirect('/') }
    if (gift.limit < 1) { return res.redirect('/') }

    const target = users.get(gift.user)
    if (target.balance < gift.amount) { return res.redirect('/') }

    // gift is valid, so claim it
    [console.log, logger]?.[process.env.LOG]?.('claimed gift')

    gift.limit -= 1
    target.balance -= gift.amount
    req.user.balance += gift.amount

    res.redirect('/')
})

app.get('/flag', async (req, res) => {
    if (req.user.balance >= Infinity) res.sendFile('flag.txt', { root: '.' })
    else res.type('text/plain').send('not enough balance...')
})

app.listen(3000, () => (
    [console.log, logger]?.[process.env.LOG]?.('listening on 3000')
))
