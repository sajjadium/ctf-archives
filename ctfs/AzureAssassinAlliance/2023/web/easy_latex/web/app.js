const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const rateLimit = require('express-rate-limit');
const ejs = require('ejs')
const jwt = require('./utils/jwt')
const crypto = require('crypto')
const fs = require('fs')
const { Store } = require('./utils/store')
const { visit } = require('./bot')

const VIP_URL = process.env.VIP_URL
    ?? console.log('no VIP_URL set, use default')
    ?? 'https://ys.mihoyo.com/'

const PORT = 3000
const notes = new Store()
const app = express()
const md5 = (data) => crypto.createHash('md5').update(data).digest('hex')

app.set('view engine', 'html')
app.engine('html', ejs.renderFile);

function sign(payload) {
    const prv_key = fs.readFileSync('prv.key')
    let token = jwt.sign(payload, prv_key, { algorithm: 'RS256' })
    return token
}

function verify(token) {
    const pub_key = fs.readFileSync('pub.key')
    try {
        jwt.verify(token, pub_key)
        return true
    } catch (e) {
        console.log(e)
        return false
    }
}

const getNonce = (l) => {
    return crypto.randomBytes(Math.ceil(l / 2)).toString('hex')
}

app.use(bodyParser.urlencoded({ extended: true }))
app.use(cookieParser())

const reportLimiter = rateLimit({
    windowMs: 5 * 1000,
    max: 1,
});

const auth = (req, res, next) => {
    let token = req.cookies.token
    if (!token) {
        res.send('login required')
        return
    }
    if (!verify(token)) {
        res.send('illegal token')
        return
    }
    let claims = jwt.decode(token)
    req.session = claims
    next()
}

app.use(express.static('static'))

app.get('/login', (req, res) => {
    return res.render('login')
})

app.post('/login', (req, res) => {
    let { username, password } = req.body

    if (md5(username) != password) {
        res.render('login', { msg: 'login failed' })
        return
    }

    let token = sign({ username, isVip: false })
    res.cookie('token', token)
    res.redirect('/')
})

app.get('/', (req, res) => {
    res.render('index.html', { login: !!req.cookies.token })
})

app.get('/preview', (req, res) => {
    let { tex, theme } = req.query
    if (!tex) {
        tex = 'Today is \\today.'
    }
    const nonce = getNonce(16)
    let base = 'https://cdn.jsdelivr.net/npm/latex.js/dist/'
    if (theme) {
        base = new URL(theme, `http://${req.headers.host}/theme/`) + '/'
    }
    res.render('preview.html', { tex, nonce, base })
})

app.post('/note', auth, (req, res) => {
    let { tex, theme } = req.body
    if (!tex) {
        res.send('empty tex')
        return
    }
    if (!theme || !req.session.isVip) {
        theme = ''
    }
    const id = notes.add({ tex, theme })
    let msg = (!req.body.theme || req.session.isVip) ? '' : 'Be VIP to enable theme setting!'
    msg += `\nYour note link: http://${req.headers.host}/note/${id}`
    msg += `\nShare it via http://${req.headers.host}/share/${id}`
    res.send(msg.trim())
})

app.get('/note/:id', (req, res) => {
    const note = notes.get(req.params.id)
    if (!note) {
        res.send('note not found');
        return
    }
    const { tex, theme } = note
    const nonce = getNonce(16)
    let base = 'https://cdn.jsdelivr.net/npm/latex.js/dist/'
    let theme_url = `http://${req.headers.host}/theme/`
    if (theme) {
        base = new URL(theme, `http://${req.headers.host}/theme/`) + '/'
    }
    res.render('note.html', { tex, nonce, base, theme_url })
})

app.post('/vip', auth, async (req, res) => {
    let username = req.session.username
    let { code } = req.body
    let vip_url = VIP_URL
    let data = await (await fetch(new URL(username, vip_url), {
        method: 'POST',
        headers: {
            Cookie: Object.entries(req.cookies).map(([k, v]) => `${k}=${v}`).join('; ')
        },
        body: new URLSearchParams({ code })
    })).text()
    if ('ok' == data) {
        res.cookie('token', sign({ username, isVip: true }))
        res.send('Congratulation! You are VIP now.')
    } else {
        res.send(data)
    }
})

app.get('/share/:id', reportLimiter, async (req, res) => {
    const { id } = req.params
    if (!id) {
        res.send('no note id specified')
        return
    }
    const url = `http://localhost:${PORT}/note/${id}`
    try {
        await visit(url)
        res.send('done')
    } catch (e) {
        console.log(e)
        res.send('something error')
    }
})

app.get('/flag', (req, res) => {
    res.send('Genshin start!')
})

app.listen(PORT, '0.0.0.0', () => {
    console.log(`listen on ${PORT}`)
})