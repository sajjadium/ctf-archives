const express = require('express')
const expressLayouts = require('express-ejs-layouts')
const mongoose = require('mongoose')
const uuid = require('uuid').v4
const flash = require('connect-flash')
const session = require('express-session')
const cookieParser = require('cookie-parser')



const BIND_ADDR = process.env.BIND_ADDR || '127.0.0.1';
const PORT = process.env.PORT || 5000
const SESSION_SECRET = process.env.SESSION_SECRET || uuid();

const app = express()

// DB config
const db = require('./helper/db').MongoURI;


mongoose.connect(db, {
    useNewUrlParser: true,
    connectTimeoutMS: 10000,
    useFindAndModify: false,
    useUnifiedTopology: true
})
    .then(() => console.log('MongoDB Connected.'))
    .catch(err => console.log(err)) 


// EJS
app.use(expressLayouts)
app.set('view engine', 'ejs')


// body parser
app.use(express.urlencoded({ extended: false }))

// cookie parser
app.use(cookieParser())

// trust first proxy for secure cookies
app.set('trust proxy', 1)

// express session
app.use(session({
    secret: SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    name: 'bookmarker-session',
    cookie: {
        secure: true,
        httpOnly: true,
        sameSite: 'none',
    },

}))

// connect flash
app.use(flash())
app.use((req, res, next) =>{
    res.locals.message = req.flash();
    next();
})

// CORP
/*
app.use((req, res, next) => {
    res.setHeader('Cross-Origin-Resource-Policy', "same-site");
    next();
});
*/

// xframe
/* 
app.use((req, res, next) => {
    res.setHeader('X-Frame-Options', "sameorigin");
    next();
});
*/ 

// COOP
app.use((req, res, next) => {
    res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
    next();
})


// csp 
app.use((req, res, next) => {
    res.header("Content-Security-Policy", "default-src 'none'; style-src *; font-src *; img-src 'self';")
    next();
})



// routes
app.use('/', require('./routes/index'))
app.use('/static', express.static(__dirname + '/static'))
app.use('/user', require('./routes/user'))



app.listen(PORT, BIND_ADDR, console.log(`Started on http://${BIND_ADDR}:${PORT}`))