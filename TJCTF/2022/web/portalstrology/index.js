const express = require('express')
const jwt = require("jsonwebtoken")
const jwk = require("node-jwk")
const axios = require('axios')
const cookieParser = require("cookie-parser")
const fs = require('fs')
const app = express()

app.use(cookieParser())

app.set('view engine', 'ejs')
app.use(express.static(`${__dirname}/static`));

app.use(express.urlencoded({ extended: false }))

const { addUser, checkUserExists, getUserApplied, authenticateUser } = require("./db/db")

const FLAG = fs.readFileSync(`${__dirname}/flag.txt`)

function check_login(req, res, next) {
    if (!req.body.username) {
        return res.render('login', { login: true, error: "Please provide a username." });
    }
    else if (!req.body.password) {
        return res.render('login', { login: true, error: "Please provide a password." });
    }
    else if (!authenticateUser(req.body.username, req.body.password)) {
        return res.render('login', { login: true, error: "Invalid Credentials" })
    }
    else {
        next()
    }
}

function generate_token(req, res, next) {
    const username = req.body.username
    const privatekey = fs.readFileSync(`${__dirname}/private/private.key`, 'utf8')
    const token = jwt.sign(
        {
            username,
        },
        privatekey,
        {
            algorithm: 'RS256',
            expiresIn: "2h",
            header: {
                alg: 'RS256',
                jku: process.env.ENV === "development" ? 'http://localhost:3000/jwks.json' : 'https://dnu-financial-aid.tjc.tf/jwks.json',
                kid: '1',
            }
        }
    )
    res.cookie("jwt", token)
    next()
}

function check_logged_in(req, res, next) {
    try {
        const token = req.cookies.jwt
        const decoded = jwt.verify(token, SECRET)
        res.redirect('/finaid')
    }
    catch {
        next()
    }
}

async function check_token(req, res, next) {
    try {
        const token = req.cookies.jwt

        const { header } = jwt.decode(token, { complete: true })
        const { kid } = header
        const jwksURI = header.jku

        await axios.get(jwksURI).then(function (response) {
            const signedKey = response.data
            const keySet = jwk.JWKSet.fromObject(signedKey)
            const key = keySet.findKeyById(kid).key.toPublicKeyPEM()

            const decoded = jwt.verify(token, key, { algorithms: ['RS256'] })

            res.locals.username = decoded.username
            res.locals.iat = decoded.iat
            next()
        })
    }
    catch {
        res.redirect('/logout')
    }
}

function check_user_applied(req, res, next) {
    if (getUserApplied(res.locals.username)) {
        res.locals.applied = true
        next()
    }
    else {
        res.locals.applied = false
        next()
    }
}

function register_user(req, res, next) {
    if (!req.body.username) {
        return res.render('login', { login: false, error: "Please provide a username." });
    }
    else if (!req.body.password) {
        return res.render('login', { login: false, error: "Please provide a password." });
    }
    else if (checkUserExists(req.body.username)) {
        return res.render('login', { login: false, error: "User already exists!" });
    }
    else {
        addUser(req.body.username, req.body.password)
        next()
    }
}

app.get('/', [check_logged_in], (req, res) => {
    res.render('login', { login: true })
})

app.get('/login', [check_logged_in], (req, res) => {
    res.render('login', { login: true })
})

app.get('/logout', (req, res) => {
    return res.clearCookie("jwt").redirect("/login")
})

app.post('/login', [check_login, generate_token], (req, res) => {
    res.redirect('/finaid')
})

app.get('/register', [check_logged_in], (req, res) => {
    res.render('login', { login: false })
})

app.post('/register', [register_user, generate_token], (req, res) => {
    res.redirect('/finaid')
})

app.get('/finaid', [check_token, check_user_applied], (req, res) => {
    if (res.locals.iat >= 1652821200) {
        res.render('finaid', { flag: `${FLAG}`, username: res.locals.username, applied: res.locals.applied })
    }
    else {
        res.render('finaid', { flag: undefined, username: res.locals.username, applied: res.locals.applied })
    }
})

app.listen(3000)
