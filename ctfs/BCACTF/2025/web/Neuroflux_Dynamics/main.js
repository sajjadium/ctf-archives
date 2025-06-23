import express from 'express'
import Database from 'better-sqlite3'

import crypto from 'node:crypto'
import { readFileSync } from 'node:fs'

const db = new Database('boxed.db', { readonly: true })

if (!db.readonly) {
    db.exec(`create table if not exists users (
        username text unique not null,
        password text not null
    ) strict`)
    db.exec(`create table if not exists products (
        name text unique not null
    ) strict`)
}

const app = express()

app.set('view engine', 'ejs')

app.use(express.urlencoded())

app.get('/', (_req, res) => {
    res.render('index', { flag: null })
})

const safeCompare = (a, b) => {
    a = Buffer.from(a, 'utf-8')
    b = Buffer.from(b, 'utf-8')

    return a.length === b.length && crypto.timingSafeEqual(a, b)
}

app.post('/', (req, res) => {
    if (typeof req.body?.username !== 'string' || typeof req.body?.password !== 'string' ||
        req.body.username.length > 100 || req.body.password.length > 100) {
        res.status(400).send('Bad Request')
        return
    }

    const user = db.prepare('select * from users where username=?').get(req.body.username)
    if (!user) {
        res.render('index', { flag: 'Wrong username' })
        return
    }

    const salt = Buffer.from(user.password, 'hex').subarray(0, 17 * 2)

    const checkHash = crypto.createHash('sha1').update(Buffer.concat([
        salt,
        Buffer.from(req.body.password, 'utf-8')
    ])).digest()

    const checkHex = Buffer.alloc(17 + checkHash.length)
    Buffer.from(salt, 'utf-8').copy(checkHex, 0, 0)
    checkHash.copy(checkHex, salt.length, 0)

    if (safeCompare(user.password, checkHex.toString('hex'))) {
        res.render('index', { flag: readFileSync('flag.txt', 'utf-8') })
    } else {
        res.render('index', { flag: 'Wrong password' })
    }
})

app.get('/register', (_req, res) => {
    res.render('register')
})

app.post('/register', (req, res) => {
    if (db.readonly) {
        res.status(403).send('Cannot register new users')
        return
    }

    const salt = crypto.randomBytes(17).toString('hex')
    const hashedPw = crypto.createHash('sha1').update(salt + req.body.password).digest()

    const hex = Buffer.alloc(17 + hashedPw.length)
    Buffer.from(salt, 'utf-8').copy(hex, 0, 0)
    hashedPw.copy(hex, salt.length, 0)

    const it = db.prepare('insert into users (username, password) values (?, ?)')
    it.run(req.body.username, hex.toString('hex'))

    res.redirect('/')
})

app.post('/search', (req, res) => {
    if (typeof req.body?.query !== 'string' || req.body.query.length > 100) {
        res.status(400).send('Bad Request')
        return
    }

    const it = db.prepare(`select * from products where name like '%${req.body.query}%'`)

    res.render('search', {
        products: JSON.stringify(it.all(), null, 4)
    })
})

app.listen(3000, () => console.log('Up on port 3000'))
