const express = require('express');

const router = new express.Router();

router.get('/', (_, res) => {
    res.render('index');
});

router.get('/login', (_, res) => {
    res.render('login', { pageName: 'Login' });
});

router.get('/register', (_, res) => {
    res.render('login', { pageName: 'Register' });
});

router.get('/post/:id', (_, res) => {
    res.render('complaint');
});

router.get('/profile', (_, res) => {
    res.render('profile');
});

router.get('/logout', (_, res) => {
    res.render('logout');
});

module.exports = router;
