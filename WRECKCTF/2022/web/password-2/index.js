const crypto = require('crypto')
const database = require('better-sqlite3')
const express = require('express')
const app = express()

FLAG = process.env.FLAG ?? 'no flag set!'

const db = new database(':memory:')
const id = () => crypto.randomBytes(16).toString('hex')

app.use(express.static('public'))
app.use(express.json())

app.post('/password', (req, res) => {
    const password = (req.body.password ?? '').toString()
    const result = db.prepare(
        `SELECT password FROM passwords WHERE password='${password}';`
    ).get()
    if (result) res.json({ success: true, flag: FLAG })
    else res.json({ success: false })
})

db.exec(`
    CREATE TABLE passwords (
        password TEXT
    );

    INSERT INTO passwords (password) VALUES ('${id()}');
    INSERT INTO passwords (password) VALUES ('${id()}');
    INSERT INTO passwords (password) VALUES ('${id()}');
    INSERT INTO passwords (password) VALUES ('${id()}');
`)

app.listen(3000)
