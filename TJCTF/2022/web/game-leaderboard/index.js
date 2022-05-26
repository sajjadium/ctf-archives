const express = require('express')
const cookieParser = require('cookie-parser')
const fs = require('fs')
const app = express()

app.use(cookieParser())

app.set('view engine', 'ejs')
app.use(express.static(`${__dirname}/public`))
app.use(express.urlencoded({ extended: false }))

const db = require('./db')

const FLAG = fs.readFileSync(`${__dirname}/flag.txt`).toString().trim()

const getLeaderboard = (minScore) => {
    const where = (typeof minScore !== 'undefined' && minScore !== '') ? ` WHERE score > ${minScore}` : ''
    const query = `SELECT profile_id, name, score FROM leaderboard${where} ORDER BY score DESC`
    const stmt = db.prepare(query)

    const leaderboard = []
    for (const row of stmt.iterate()) {
        if (leaderboard.length === 0) {
            leaderboard.push({ rank: 1, ...row })
            continue
        }
        const last = leaderboard[leaderboard.length - 1]
        const rank = (row.score == last.score) ? last.rank : last.rank + 1
        leaderboard.push({ rank, ...row })
    }

    return leaderboard
}

app.get('/', (req, res) => {
    const leaderboard = getLeaderboard()
    return res.render('leaderboard', { leaderboard })
})

app.post('/', (req, res) => {
    const leaderboard = getLeaderboard(req.body.filter)
    return res.render('leaderboard', { leaderboard })
})

app.get('/user/:userID', (req, res) => {
    const leaderboard = getLeaderboard()
    const total = leaderboard.length

    const profile = leaderboard.find(x => x.profile_id == req.params.userID)
    if (typeof profile === 'undefined') {
        return res.render('user_info', { notFound: true })
    }

    const flag = (profile.rank === 1) ? FLAG : 'This is reserved for winners only!'
    return res.render('user_info', { total, flag, ...profile })
})

app.listen(3000, () => {
    console.log('server started')
})
