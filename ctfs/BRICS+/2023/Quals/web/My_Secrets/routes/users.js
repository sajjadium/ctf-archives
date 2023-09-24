const express = require('express');
const router = express.Router();
const User = require('../models/user');
const bcrypt = require('bcrypt');

// Register Route
router.get('/register', (req, res) => {
    res.render('register',{language: req.session.lang});
});

router.post('/register', async (req, res) => {
    try {
        const hashedPassword = await bcrypt.hash(req.body.password, 10);
        const user = new User({
            username: req.body.username,
            password: hashedPassword
        });
        await user.save();
        res.redirect('/users/login');
    } catch (error) {
        console.error(error);
        res.render('error', { message: 'An error occurred while registering.',language: req.session.lang });
    }
});

// Login Route
router.get('/login', (req, res) => {
    res.render('login',{language: req.session.lang});
});

router.post('/login', async (req, res) => {
    const user = await User.findOne({ username: req.body.username });
    if (user && await bcrypt.compare(req.body.password, user.password)) {
        req.session.user = user; // Store user in session
        res.redirect('/posts');
    } else {
        res.render('error', { message: 'Invalid username or password.',language: req.session.lang });
    }
});

// Logout Route
router.get('/logout', (req, res) => {
    req.session = undefined;
    res.redirect("/")
});

module.exports = router;
