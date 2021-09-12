const express = require('express')
const db = require("../db");

const router = express.Router()

router.get('/login', (req, res) => {
    res.render('login')
})

router.get('/register', (req, res) => {
    res.render('register')
})

router.post('/login', async (req, res) => {
    let {username, password} = req.body
    let rec = await db.Users.find({username: username, password: password})
    if (rec) {
        if (rec.username === username && rec.password === password) {
            res.cookie('token', rec, {signed: true})
            res.redirect('/shop')
        } else {
            res.render('login', {error: 'You Bad Bad >_<'})
        }
    } else {
        res.render('login', {error: 'Login Failed!'})
    }
})

router.post('/register', async (req, res) => {
    let {username, password} = req.body
    if (typeof(username) !== 'string')
        return res.status(400)
    let rec = await db.Users.find({username: username})
    if (rec)
        return res.render('register', {error: 'Duplicate User!'})
    await db.Users.add(username, password, false)
    return res.redirect('/user/login')
})

module.exports = router