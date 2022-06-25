const app = require('express')()
const bodyParser = require('body-parser')
const session = require('express-session')
const admin = require('./admin')
const mongoose = require('mongoose')
const rand = require('string-random')
const crypto = require('crypto')

const LISTEN = '0.0.0.0'
const PORT = 8000
const config = require('./config')
const FLAG = config.FLAG
const FAKE_FLAG = config.FAKE_FLAG
const MONGO_URL = 'mongodb://mongodb:27017/ctf'
const SECRET = rand(32, '0123456789abcdef')


const ValidateToken = (Token) => {
    var sha256 = crypto.createHash('sha256');
    return sha256.update(Math.sin(Math.floor(Date.now() / 1000)).toString()).digest('hex') === Token;
}

mongoose.connect(MONGO_URL)
const User = mongoose.model("users", new mongoose.Schema({
    username: String,
    password: String,
    isAdmin: Boolean
}))

app.set('view engine', 'ejs')
app.use(session({
    secret: SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false },
}))
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.send('hello world')
})

app.get('/login', (req, res) => {
    res.render('login', {})
})

app.post('/admin', (req, res) => {
    let url = req.body.url ? req.body.url : 'http://pumpk1n.com'
    admin.view(url)
        .then(() => { res.send(url) })
        .catch(e => { res.send(e) })
})

app.get('/home', (req, res) => {
    if (!req.session.user) {
        res.redirect('/login')
        return
    }
    res.render('home', { user: req.session.user })
})

app.post('/login', (req, res) => {
    let username = req.body.username
    let password = req.body.password
    console.log("login", username, password)
    if (typeof username !== 'string' || typeof password !== 'string') {
        res.render('login', { error: "wafed" })
        return
    }

    User.find({ username: username, password: password }, (err, user) => {
        if (err) {
            res.render('login', { error: err })
            return
        }
        if (user.length > 0) {
            req.session.user = username
            res.redirect('home')
        } else {
            res.render('login', { error: "login failed" })
        }
    })
})

app.get('/register', (req, res) => {
    res.render('register', {})
})

app.post('/register', (req, res) => {
    let username = req.body.username
    let password = req.body.password
    if (typeof username !== 'string' || typeof password !== 'string') {
        res.render('login', { error: "wafed" })
        return
    }
    const newuser = new User({
        username: username,
        password: password,
        isAdmin: false
    })
    User.find({ username: username }, (err, user) => {
        if (err) {
            res.render('register', { error: err })
            return
        }
        if (user.length > 0) {
            res.render('register', { error: "user already exists!" })
        } else {
            newuser.save()
            res.redirect('login', 302)
        }

    })
})

app.post('/beAdmin', (req, res) => {
    if (req.session.user != 'admin') {
        res.send("sorry, only admin can be admin")
        return
    }
    const username = req.body.username
    const csrftoken = req.body.csrftoken
    if (ValidateToken(csrftoken)) {
        User.updateMany({ username: username }, { isAdmin: true },
            (err, users) => {
                if (err) {
                    res.send('something error when being admin')
                    return
                }
                if (users.length == 0) {
                    res.send('no one can be admin')
                } else {
                    res.send('wow success wow')
                }
            }
        )
    } else {
        res.send('validate error')
    }
})

app.get('/flag', (req, res) => {
    if (!req.session.user) {
        res.send(FAKE_FLAG)
        return
    }
    User.findOne({ username: req.session.user }, (err, user) => {
        if (err) {
            res.send({ err: err })
            return
        }
        if (user.isAdmin) {
            // part 1
            res.send(FLAG.substring(0, 16))
        } else {
            res.send(FAKE_FLAG)
        }
    })
})

app.listen(PORT, LISTEN, () => {
    console.log(`listening ${LISTEN}:${PORT}...`)
})