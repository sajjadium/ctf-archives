import crypto from 'node:crypto';

import { Sequelize, DataTypes } from 'sequelize';
import express from 'express';
import session from 'express-session';
import basicAuth from 'express-basic-auth';

const FLAG = process.env.FLAG || 'nek0pts{FAKE_FLAG}';
const CHALL_NAME = 'Warmuprofile';

const { CS_USERNAME, CS_PASSWORD } = process.env;

// connect to DB
const sequelize = new Sequelize('sqlite::memory:');
try {
    await sequelize.authenticate();
} catch (error) {
    console.error('Unable to connect to the database:', error);
}

// set up DB
const User = sequelize.define('User', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    profile: {
        type: DataTypes.STRING
    }
}, {});
await User.sync({ force: true });
await User.create({
    username: 'admin',
    password: crypto.randomUUID(),
    profile: 'Hi, I am admin.'
});

// set up Web server
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: crypto.randomUUID(),
    resave: false,
    saveUninitialized: true,
    cookie: {
        secure: false
    }
}));
app.set('view engine', 'ejs');
app.use(express.static('public'));

// set BASIC auth for container spawner
// you don't need to care about this on your local environment
if (CS_USERNAME && CS_PASSWORD) {
    app.use(basicAuth({
        users: {
            [CS_USERNAME]: CS_PASSWORD
        },
        challenge: true,
        realm: CS_USERNAME
    }));
}

// set flash message
function flash(req, mes) {
    req.session.flash = mes;
}

// get flash message
function getFlash(req) {
    const res = req.session?.flash;
    if (res) {
        delete req.session.flash;
    }

    return res;
}

// if this function is given as callback,
// then users cannot the route when not logged in
function needAuth(req, res, next) {
    if (!req.session.loggedIn) {
        flash(req, 'not logged in');
        return res.redirect('/');
    }

    next();
};

app.get('/', async (req, res) => {
    let user = null;
    if (req.session.loggedIn) {
        user = await User.findOne({
            where: { username: req.session.username }
        });
    }

    res.render('index', {
        chall_name: CHALL_NAME, flash: getFlash(req),
        loggedIn: req.session.loggedIn, user
    });
});

app.get('/login', (req, res) => {
    res.render('login', { chall_name: CHALL_NAME, flash: getFlash(req) });
});

app.post('/login', async (req, res) => {
    // make sure given username and password are valid
    const { username, password } = req.body;
    if (!username || !password) {
        flash(req, 'username or password not provided');
        return res.redirect('/login');
    }
    if (typeof username !== 'string' || typeof password !== 'string') {
        flash(req, 'invalid username or password');
        return res.redirect('/login');
    }

    // then check if there is a user with given username nad password
    const user = await User.findOne({
        where: { username, password }
    });
    if (user == null) {
        flash(req, 'invalid username or password');
        return res.redirect('/login');
    }

    // okay, it exists. store user information in session
    req.session.loggedIn = true;
    req.session.username = user.username;

    return res.redirect('/');
});

app.get('/register', (req, res) => {
    res.render('register', { chall_name: CHALL_NAME, flash: getFlash(req) });
});

app.post('/register', async (req, res) => {
    // make sure given username and password are valid
    const { username, password, profile } = req.body;
    if (!username || !password || !profile) {
        flash(req, 'username, password, or profile not provided');
        return res.redirect('/register');
    }
    if (typeof username !== 'string' || typeof password !== 'string' || typeof profile !== 'string') {
        flash(req, 'invalid username, password, or profile');
        return res.redirect('/register');
    }

    // make sure that the requested username does not exist
    const user = await User.findOne({
        where: { username }
    });
    if (user != null) {
        flash(req, 'user exists');
        return res.redirect('/register');
    }

    // okay, create a user
    await User.create({
        username, password, profile
    });

    req.session.loggedIn = true;
    req.session.username = username;

    return res.redirect('/');
});

app.get('/user/:username', async (req, res) => {
    const user = await User.findOne({
        where: { username: req.params.username }
    });

    if (user == null) {
        flash(req, 'user not found');
        return res.redirect('/');
    }

    return res.render('user', { chall_name: CHALL_NAME, flash: getFlash(req), user });
});

app.get('/user/:username/delete', needAuth, async (req, res) => {
    const { username } = req.params;
    const { username: loggedInUsername } = req.session;
    if (loggedInUsername !== 'admin' && loggedInUsername !== username) {
        flash(req, 'general user can only delete itself');
        return res.redirect('/');
    }

    const user = await User.findOne({
        where: { username: loggedInUsername }
    });

    res.render('delete', {
        chall_name: CHALL_NAME, flash: getFlash(req),
        loggedIn: req.session.loggedIn, user, username
    });
});

app.post('/user/:username/delete', needAuth, async (req, res) => {
    const { username } = req.params;
    const { username: loggedInUsername } = req.session;
    if (loggedInUsername !== 'admin' && loggedInUsername !== username) {
        flash(req, 'general user can only delete itself');
        return res.redirect('/');
    }

    // find user to be deleted
    const user = await User.findOne({
        where: { username }
    });

    await User.destroy({
        where: { ...user?.dataValues }
    });

    // user is deleted, so session should be logged out
    req.session.destroy();
    return res.redirect('/');
});

app.get('/logout', needAuth, (req, res) => {
    req.session.destroy();
    return res.redirect('/');
});

app.get('/flag', needAuth, (req, res) => {
    if (req.session.username !== 'admin') {
        flash(req, 'only admin can read the flag');
        return res.redirect('/');
    }

    return res.render('flag', { chall_name: CHALL_NAME, flash: getFlash(req), flag: FLAG });
});

app.listen(3000, () => {
    console.log('started');
});