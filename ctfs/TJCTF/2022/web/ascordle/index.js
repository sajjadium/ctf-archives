const express = require('express')

const app = express()
app.use(express.json())

const db = require('./db')
const { randStr } = require('./utils')

const fs = require('fs')
const flag = fs.readFileSync('flag.txt').toString().trim()

const wrong = new Array(16).fill("N")
const right = new Array(16).fill("G")

const randomize = () => {
    const word = randStr(16).replaceAll("'", "''")
    const query = db.prepare(`UPDATE answer SET word = '${word}'`)
    query.run() // haha now you will never get the word
}

const waf = (str) => {
    const banned = ["OR", "or", "--", "=", ">", "<"]
    for (const no of banned) {
        if (str.includes(no)) return false
    }
    return true
}

const getWord = () => {
    const query = db.prepare('SELECT * FROM answer')
    return query.get()
}

const checkWord = (word) => {
    const query = db.prepare(`SELECT * FROM answer WHERE word = '${word}'`)
    return typeof query.get() !== 'undefined'
}

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

app.post('/guess', (req, res) => {
    if (typeof req.body.word !== 'string') {
        return res.status(400).end('???')
    }

    randomize()

    const word = req.body.word
    if (!waf(word)) {
        return res.json({
            check: false,
            flag: null,
            sql: true,
            colors: wrong,
        })
    }

    const { word: correct } = getWord()

    try {
        if (checkWord(word)) {
            return res.json({
                check: true,
                flag: flag,
                sql: false,
                colors: right,
            })
        }
    } catch (e) {
        return res.json({
            check: false,
            flag: null,
            sql: false,
            colors: wrong,
        })
    }

    const colors = Array.from(wrong)
    const maybe = new Map()
    for (let i = 33; i <= 126; i++) {
        maybe.set(String.fromCharCode(i), 0)
    }
    for (let i = 0; i < 16; i++) {
        const c = correct.charAt(i)
        if (word.charAt(i) === c) {
            colors[i] = "G"
        } else {
            maybe.set(c, maybe.get(c) + 1)
        }
    }
    for (let i = 0; i < 16; i++) {
        if (colors[i] === "G") continue
        const c = word.charAt(i)
        if (maybe.get(c) > 0) {
            colors[i] = "Y"
            maybe.set(c, maybe.get(c) - 1)
        }
    }

    return res.json({
        check: false,
        flag: null,
        sql: false,
        colors: colors,
    })
})

app.listen(3000, '0.0.0.0')
