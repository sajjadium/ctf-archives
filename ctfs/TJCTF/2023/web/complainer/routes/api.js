const express = require('express');
const { createPost, createUser, login, verifySession, deleteSession, getUser, getPost } = require('../api.js');

const router = new express.Router();

router.use(express.json());

const verifySessionMiddleware = (req, res, next) => {
    const auth = req.headers.authorization;
    if (!auth) {
        res.status(400).json({
            ok: false,
            error: 'No authorization header.'
        });

        return;
    }

    const [userId, sessionId] = auth.split(' ')[1].split(':');
    if (!verifySession(userId, sessionId)) {
        res.status(400).json({
            ok: false,
            error: 'Invalid session.'
        });
    } else {
        res.locals.userId = userId;
        res.locals.sessionId = sessionId;
        next();
    }
};

router.post('/post', verifySessionMiddleware, (req, res) => {
    const postId = createPost(res.locals.userId, req.body.body);

    res.json({
        postId,
        ok: true
    });
});

router.post('/register', (req, res) => {
    try {
        createUser(req.body.username, req.body.password);
    } catch (err) {
        res.json({
            ok: false,
            error: err
        });

        return;
    }

    const { userId, sessionId } = login(req.body.username, req.body.password);

    res.json({
        userId,
        sessionId,
        ok: true
    });
});

router.post('/login', (req, res) => {
    try {
        const { userId, sessionId } = login(req.body.username, req.body.password);

        res.json({
            userId,
            sessionId,
            ok: true
        });
    } catch (err) {
        res.json({
            ok: false,
            error: err
        });
    }

});

router.post('/logout', verifySessionMiddleware, (req, res) => {
    deleteSession(res.locals.userId);

    res.json({
        ok: true
    });
});

router.get('/post/:id', (req, res) => {
    const post = getPost(req.params.id);

    if (!post) {
        res.status(404).json({
            error: 'Post not found.',
            ok: false
        });
    } else {
        res.json({
            post,
            ok: true
        });
    }
});

router.get('/verify', verifySessionMiddleware, (_, res) => {
    res.json({
        ok: true
    });
});

router.get('/profile', verifySessionMiddleware, (req, res) => {
    res.json({
        user: getUser(res.locals.userId),
        ok: true
    });
});

module.exports = router;
