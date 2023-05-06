const path = require('path')
const fs = require('fs')
const express = require('express')
const db = require('../db')
const pug = require('pug')

const router = express.Router()

const checkLogin = (req, res, next) => {
    if (req.signedCookies.token)
        next()
    else
        res.render('error', {error: 'You must login!'})
}

const checkActive = (req, res, next) => {
    if (req.signedCookies.token.active)
        next()
    else
        res.render('error', {error: 'Your account is not active!'})
}


router.get('/', checkLogin, async (req, res) => {
    let candies = await db.Candies.list()
    res.render('shop', {candies: candies})
})

router.get('/order', checkLogin, checkActive, async (req, res) => {
    let {id} = req.query
    let candy = await db.Candies.find({id: id})
    res.render('order', {username: req.signedCookies.token.username, candy: candy})
})

router.post('/order', checkLogin, checkActive, async (req, res) => {
    let {username, candyname, address} = req.body
    let tpl_path = path.join(__dirname, '../views/confirm.pug')
    fs.readFile(tpl_path, (err, result) => {
        if (err) {
            res.render('error', {error: 'Fail to load template!'})
        } else {
            let tpl = result
                .toString()
                .replace('USERNAME', username)
                .replace('CANDYNAME', candyname)
                .replace('ADDRESS', address)
            res.send(pug.render(tpl, options={filename: tpl_path}))
        }
    })
})

router.get('/thanks', checkLogin, checkActive, async (req, res) => {
    res.render('thanks')
} )

module.exports = router