const path = require('path')
const mongoose = require('mongoose')
const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')
const passport = require('passport')
const { engine } = require('express-handlebars')
const { Strategy: JwtStrategy } = require('passport-jwt')

const User = require('../models/user')
const Note = require('../models/note')

function connectDB(DB_URI, dbName) {
    return new Promise((res, _) => {
        mongoose.connect(DB_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            dbName
        }).then(() => res())
    })
}

async function initApp() {
    const app = express()

    app.use(bodyParser.json())
    app.use(cookieParser())

    app.use(passport.initialize())
    passport.use('user-local', User.createStrategy())
    const jwtOpts = {
        secretOrKey: process.env.JWT_SECRET,
        jwtFromRequest: (req) => req?.cookies?.['jwt'],
        algorithms: ['HS256']
    }
    passport.use(
        new JwtStrategy(jwtOpts, (payload, next) => {
            User.findOne({ _id: payload.userId })
                .then((user) => {
                    next(null, { userId: user._id } || false)
                })
                .catch((_) => next(null, false))
        })
    )

    let admin = await User.findOne({ username: 'admin' })
    if(!admin) {
        admin = new User({ username: 'admin' })
        await admin.save()
    }
    let note = await Note.findOne({ noteId: 1337 })
    if(!note) {
        const FLAG = process.env.FLAG || 'DUCTF{test_flag}'
        note = new Note({ owner: admin._id, noteId: 1337, contents: FLAG })
        await note.save()
        admin.notes.push(note)
        await admin.save()
    }

    app.engine('hbs', engine({
        extname: '.hbs',
        defaultLayout: 'main'
    }))
    app.set('view engine', 'hbs')
    app.set('views', path.join(__dirname, '../views'))

    app.use('/', require('./routes'))

    app.use('/', (req, res) => {
        res.status(404)
        if(req.accepts('html')) {
            return res.render('404')
        }
        if(req.accepts('json')) {
            return res.json({ success: false, error: 'Not found' })
        }
        return res.type('txt').send('Not found')
    })

    return app
}

module.exports = {
    connectDB,
    initApp
}
