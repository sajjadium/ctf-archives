const express = require('express')
const expressLayouts = require('express-ejs-layouts')
const mongoose = require('mongoose')
const uuid = require('uuid').v4
const flash = require('connect-flash')
const session = require('express-session')
const cookieParser = require('cookie-parser')



const BIND_ADDR = process.env.BIND_ADDR || 'localhost'
const PORT = process.env.PORT || 5000
const SESSION_SECRET = process.env.SESSION_SECRET || uuid();

const app = express()

// DB config
const db = require('./helper/db').MongoURI;


mongoose.connect(db, {
    connectTimeoutMS: 10000,
})
.then(() => console.log('MongoDB Connected.'))
.catch(err => console.log(err)) 


// EJS
app.use(expressLayouts)
app.set('view engine', 'ejs')

// set title for templates 
app.locals.title = 'Päääds'
app.locals.domain=process.env.DOMAIN

// body parser
app.use(express.urlencoded({ extended: false }))

// cookie parser
app.use(cookieParser())


// COOP
app.use((req, res, next) => {
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    next();
})

// csp 
app.use((req, res, next) => {
    res.header("Content-Security-Policy", "default-src 'none'; script-src 'sha256-juw/gmBpJMpi5MGvXfSxKuFz+3kEuCFiQfC419Y+v1A=';  style-src *; font-src *; img-src * data:; frame-ancestors 'none'; report-uri /report");
    next();
})

app.post('/report', (req, res) => {
    // add logging here
    return res.send('ok')
})



// trust first proxy for secure cookies
app.set('trust proxy', 1)

// express session
app.use(session({
    secret: SESSION_SECRET,
    resave: true,
    saveUninitialized: true,
    name: 'paaad-session',
    cookie: {
        secure: true,
        httpOnly: true,
        sameSite: 'strict',
        domain: '.' + (process.env.DOMAIN),
    },

}))

// connect flash
app.use(flash())
app.use((req, res, next) =>{
    res.locals.message = req.flash();
    next();
})



// routes
app.use('/', require('./routes/pad'))
app.use('/static', express.static(__dirname + '/static'))
app.use('/user', require('./routes/user'))



app.listen(PORT, BIND_ADDR, console.log(`Started on http://${BIND_ADDR}:${PORT}`))