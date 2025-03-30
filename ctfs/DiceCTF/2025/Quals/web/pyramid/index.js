const express = require('express')
const crypto = require('crypto')
const app = express()

const css = `
    <link
        rel="stylesheet"
        href="https://unpkg.com/axist@latest/dist/axist.min.css"
    >
`

const users = new Map()
const codes = new Map()

const random = () => crypto.randomBytes(16).toString('hex')
const escape = (str) => str.replace(/</g, '&lt;')
const referrer = (code) => {
    if (code && codes.has(code)) {
        const token = codes.get(code)
        if (users.has(token)) {
            return users.get(token)
        }
    }
    return null
}

app.use((req, _res, next) => {
    const token = req.headers.cookie?.split('=')?.[1]
    if (token) {
        req.token = token
        if (users.has(token)) {
            req.user = users.get(token)
        }
    }
    next()
})

app.get('/', (req, res) => {
    res.type('html')

    if (req.user) {
        res.end(`
            ${css}
            <h1>Account: ${escape(req.user.name)}</h1>
            You have <strong>${req.user.bal}</strong> coins.
            You have referred <strong>${req.user.ref}</strong> users.

            <hr>

            <form action="/code" method="GET">
                <button type="submit">Generate referral code</button>
            </form>
            <form action="/cashout" method="GET">
                <button type="submit">
                    Cashout ${req.user.ref} referrals
                </button>
            </form>
            <form action="/buy" method="GET">
                <button type="submit">Purchase flag</button>
            </form>
        `)
    } else {
        res.end(`
            ${css}
            <h1>Register</h1>
            <form action="/new" method="POST">
                <input name="name" type="text" placeholder="Name" required>
                <input
                    name="refer"
                    type="text"
                    placeholder="Referral code (optional)"
                >
                <button type="submit">Register</button>
            </form>
        `)
    }
})

app.post('/new', (req, res) => {
    const token = random()

    const body = []
    req.on('data', Array.prototype.push.bind(body))
    req.on('end', () => {
        const data = Buffer.concat(body).toString()
        const parsed = new URLSearchParams(data)
        const name = parsed.get('name')?.toString() ?? 'JD'
        const code = parsed.get('refer') ?? null

        // referrer receives the referral
        const r = referrer(code)
        if (r) { r.ref += 1 }

        users.set(token, {
            name,
            code,
            ref: 0,
            bal: 0,
        })
    })

    res.header('set-cookie', `token=${token}`)
    res.redirect('/')
})

app.get('/code', (req, res) => {
    const token = req.token
    if (token) {
        const code = random()
        codes.set(code, token)
        res.type('html').end(`
            ${css}
            <h1>Referral code generated</h1>
            <p>Your code: <strong>${code}</strong></p>
            <a href="/">Home</a>
        `)
        return
    }
    res.end()
})

// referrals translate 1:1 to coins
// you receive half of your referrals as coins
// your referrer receives the other half as kickback
//
// if your referrer is null, you can turn all referrals into coins
app.get('/cashout', (req, res) => {
    if (req.user) {
        const u = req.user
        const r = referrer(u.code)
        if (r) {
            [u.ref, r.ref, u.bal] = [0, r.ref + u.ref / 2, u.bal + u.ref / 2]
        } else {
            [u.ref, u.bal] = [0, u.bal + u.ref]
        }
    }
    res.redirect('/')
})

app.get('/buy', (req, res) => {
    if (req.user) {
        const user = req.user
        if (user.bal > 100_000_000_000) {
            user.bal -= 100_000_000_000
            res.type('html').end(`
                ${css}
                <h1>Successful purchase</h1>
                <p>${process.env.FLAG}</p>
            `)
            return
        }
    }
    res.type('html').end(`
        ${css}
        <h1>Not enough coins</h1>
        <a href="/">Home</a>
    `)
})

app.listen(3000)
