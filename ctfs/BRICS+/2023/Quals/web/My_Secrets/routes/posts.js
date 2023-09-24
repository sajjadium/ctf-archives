const express = require('express');
const router = express.Router();
const Post = require('../models/post');

const isAuthenticated = (req, res, next) => {
    if (req.session.user) {
        return next();
    }
    res.redirect('/users/login');
};

// Display all posts
router.get('/', isAuthenticated, async (req, res) => {
    try {
        const user = req.session.user;
        const posts = await Post.find({ user: user._id });
        res.render('post', { posts, user,language: req.session.lang });
    } catch (error) {
        res.render('error', { message: 'Error fetching posts',language: req.session.lang });
    }
});

router.get('/add', (req, res) => {
    res.render('addPost',{language: req.session.lang});
});

// Add a new post
router.post('/add', isAuthenticated, async (req, res) => {
    const { title, content } = req.body;
    try {
        const user = req.session.user;
        await Post.create({ title, content, user: user._id });
        res.redirect('/posts');
    } catch (error) {
        res.render('error', { message: 'Error adding post',language: req.session.lang });
    }
});

// Search posts by title
router.get('/search', isAuthenticated, async (req, res) => {
    const { searchTerm } = req.query;

    try {
        const user = req.session.user;
        const posts = await Post.find({ title: { $regex: new RegExp(searchTerm, 'i') }, user: user._id }).
                            maxTimeMS(1000).
                            orFail();
        res.render('searchResults', { posts, user,language: req.session.lang });
    } catch (error) {
        // For debug only
        res._headers={'Timing-Allow-Origin':'https://google.com'}
        res.render('error', { message: 'Error searching for notes',language: req.session.lang });
    }
});

module.exports = router;
