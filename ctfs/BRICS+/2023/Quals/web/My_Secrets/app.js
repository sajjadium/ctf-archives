const express = require('express');
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const session = require('cookie-session');
const helmet = require('helmet'); // Add security headers


app.enable('trust proxy');


// Set up view engine and views directory
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Set up static file serving
app.use(express.static(path.join(__dirname, 'public')));

// Body parser middleware
app.use(bodyParser.urlencoded({ extended: true }));

// Session middleware
app.use(session({
    secret: process.env.SECRET, 
    resave: true,
    saveUninitialized: true
}));

// Stable timings
app.use("/",function (req, res, next) {
    if(req.query.lang)
        req.session.language = req.query.lang
    res.links({preload: "/images/logo.jpg"})
    res.links({preload: "/script/script.css"})
    res.links({preload: "/styles/style.css"})
    res.links({preload: req.session.language?`/styles/${req.session.language}.css`:"/styles/russian.css"})
    next();
})
// Security headers middleware
//app.use(helmet({frameguard: false}));

// Database connection (assuming you have a db.js file)
require('./db');

// Routes
const indexRouter = require('./routes/index');
const postsRouter = require('./routes/posts');
const usersRouter = require('./routes/users');
const languageRouter = require('./routes/language');
const reportRouter = require('./routes/report')
app.use('/', indexRouter);
app.use('/posts', postsRouter);
app.use('/users', usersRouter);
app.use('/setLanguage', languageRouter);
app.use('/report', reportRouter)
// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
