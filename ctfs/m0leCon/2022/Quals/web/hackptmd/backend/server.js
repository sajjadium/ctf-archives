const express = require('express')
const { v4: uuidv4 } = require('uuid')
const jwt = require('jsonwebtoken')
const cookieParser = require('cookie-parser')
const fetch = require('cross-fetch')
const csrf = require('csurf')
require('express-async-errors')
const sqlite3 = require('sqlite3')
const { open } = require('sqlite')

const app = express()
const port = 4000

const JWT_SECRET_KEY = uuidv4()

let db = undefined;

(async () => {
    // open the database
    db = await open({
        filename: ':memory:',
        driver: sqlite3.Database
    })
})().then(async () => {
    await db.exec('CREATE TABLE users (username VARCHAR(50), password VARCHAR(50), PRIMARY KEY (username))')
    await db.exec('CREATE TABLE documents (id VARCHAR(40), owner VARCHAR(50), title TEXT, data TEXT, PRIMARY KEY(id) )')

    await db.run('INSERT INTO users (username, password) VALUES ("admin", ?)', [process.env.ADMIN_PASSWORD])
    await db.run('INSERT INTO documents (id, owner, title, data) VALUES (?, "admin", "flag", ?)', [uuidv4(), process.env.FLAG])
})

app.use(express.json())
app.use(cookieParser())


const csrfProtection = csrf({ cookie: true })
app.use(csrfProtection);

app.get('/api/getCSRFToken', (req, res) => {
    res.json({ CSRFToken: req.csrfToken() });
});

app.use((req, res, next) => {
    if (req.cookies.session) {
        try {
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET_KEY)
            req.loggedUser = decoded.username
        } catch (err) {
            req.loggedUser = undefined
            res.clearCookie('session')
        }
    }
    next()
})


app.get('/api/document/:id', async (req, res) => {
    const result = await db.get('SELECT title, owner, data  FROM documents WHERE id = ?', req.params.id)

    if (!result) {
        return res.status(404).json({ error: 'not found' })
    }

    return res.json(result)
})


app.post('/api/login', async (req, res) => {
    const { username, password } = req.body

    if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'bad data' })
    }

    const result = await db.get('SELECT password FROM users WHERE username = ?', username)

    if (!result || password !== result.password) {
        return res.status(400).json({ error: 'wrong username or password' })
    }

    const token = jwt.sign({ username }, JWT_SECRET_KEY)
    res.cookie('session', token)
    res.json({ message: 'logged in' })
})

app.post('/api/signup', async (req, res) => {
    const { username, password } = req.body

    if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).json({ error: 'bad data' })
    }

    try {
        await db.run(
            'INSERT INTO users (username, password) VALUES (?,?)',
            [username, password]
        )
        return res.json({ message: 'done' })
    } catch (error) {
        if (error.errno === 19) {
            return res.status(400).json({ error: 'Username not available' })
        } else {
            return res.status(500).json({ error: 'Something is wrong' })
        }
    }
})

app.get('/api/logout', async (req, res) => {
    res.clearCookie('session')
    res.json({ message: 'ok' })
})


// require login
app.use((req, res, next) => {
    if (!req.loggedUser) {
        return res.status(403).json({ error: 'login required' })
    }
    next()
})

app.post('/api/document/:id', async (req, res) => {

    const new_data = req.body.data

    if (typeof new_data !== 'string') {
        return res.status(400).json({ error: 'bad data' })
    }

    const result = await db.run(
        'UPDATE documents SET data = ? WHERE id = ? AND owner = ?',
        [new_data, req.params.id, req.loggedUser]
    )

    if (result.changes === 0) {
        return res.status(404).json({ error: 'failed' })
    }

    return res.json({ message: 'done' })
})

app.post('/api/report/:id', async (req, res) => {

    const post = await db.get('SELECT id FROM documents WHERE id = ?', req.params.id)

    if (!post) {
        return res.status(404).json({ error: 'not found' })
    }


    try {
        const link = process.env.WEBAPP_URL + '/document/' + post.id

        const r = await fetch(process.env.BOT_URL, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'url': link })
        }).then(r => r.text())
        console.log(r)

    } catch (error) {
        return res.status(500).json({ error: 'Error: ' + error })
    }

    return res.json({ message: 'done' })
})

app.get('/api/document', async (req, res) => {

    const result = await db.all('SELECT id, title FROM documents WHERE owner = ?', req.loggedUser)
    return res.json(result)
})


app.post('/api/document', async (req, res) => {
    const title = req.body.title
    const id = uuidv4()

    if (typeof title !== 'string' || title.length > 100) {
        return res.status(400).json({ error: 'bad data' })
    }

    const result = await db.run(
        'INSERT INTO documents (id, owner, title, data) VALUES (?,?,?,"")',
        [id, req.loggedUser, title]
    )
    return res.json({ message: 'done', id: id })
})


// csrf error handling
app.use(function (err, req, res, next) {
    if (err.code !== 'EBADCSRFTOKEN') return next(err)

    res.status(400).json({ error: 'invalid CSRF token' })
})


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})