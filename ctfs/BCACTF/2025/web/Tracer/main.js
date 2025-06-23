import express from 'express'

import { resolve } from 'path'
import { readFileSync } from 'fs'

const flag = readFileSync('flag.txt', 'utf-8')

const app = express()

app.use(express.urlencoded({ extended: true }))

app.get('/', (_req, res) => {
    res.sendFile(resolve('index.html'))
})

const caseInsensitiveCompare = (a, b) => {
    if (!a.length && !b.length) {
        return true
    } else if (a.length !== b.length || a[0].toLowerCase() !== b[0].toLowerCase()) {
        return false
    }

    return caseInsensitiveCompare(a.slice(1), b.slice(1))
}

app.post('/', (req, res) => {
    if (req.body?.value?.length > 100) {
        res.status(400).send('Bad Request')
        return
    }

    if (caseInsensitiveCompare(flag, req.body.value)) {
        res.status(200).send('Correct')
    } else {
        res.status(200).send('Incorrect')
    }
})

process.on('uncaughtException', err => {
    console.error(err)
})

app.listen(3000, console.log('Up on port 3000'))
