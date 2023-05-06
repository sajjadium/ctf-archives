const express = require('express')
const router = express.Router()
const passport = require('passport')
const JWT = require('jsonwebtoken')

const User = require('../models/user')
const Note = require('../models/note')

const ensureAuthed = (req, res, next) => {
    passport.authenticate('jwt', { session: false, failureRedirect: '/login' })(req, res, next)
}

router.get('/', (req, res, next) => {
    passport.authenticate('jwt', async (err, r) => {
        let { userId } = r
        if(!userId) {
            return res.render('home', {
                isLoggedIn: false,
            })
        }

        const user = await User.findById(userId).populate('notes').exec()
        const notes = []
        for(let n of user.notes) {
            notes.push({ noteId: n.noteId, contents: n.contents })
        }
        return res.render('home', {
            isLoggedIn: true,
            username: user.username,
            notes: notes
        })
    })(req, res, next)
})

router.get('/register', (req, res) => {
    return res.render('register')
})

router.post('/register', (req, res, next) => {
    let { username, password } = req.body
    if(!username || !password) {
        return next({ message: 'Missing username or password' })
    }

    if(password.length <= 4) {
        return next({ message: 'Password should be more than 4 characters' })
    }

    User.register(new User({ username }), password, (err, user) => {
        if(err && err.toString().includes('already registered')) {
            return next({ message: 'Account already registered with that username' })
        } else if(err) {
            return next({ message: 'Error while registering user' })
        }

        const token = JWT.sign({
            userId: user._id
        }, process.env.JWT_SECRET, {
            algorithm: 'HS256',
            expiresIn: '7d'
        })

        res.cookie('jwt', token, { httpOnly: true })

        return res.json({
            success: true,
            message: 'Successfully registered.'
        })
    })
})

router.get('/login', (req, res) => {
    return res.render('login')
})

router.post('/login', (req, res, next) => {
    passport.authenticate('user-local', (_, user, err) => {
        if(err) {
            return next({ message: err.message })
        }

        const token = JWT.sign({
            userId: user._id
        }, process.env.JWT_SECRET, {
            algorithm: 'HS256',
            expiresIn: '7d'
        })

        res.cookie('jwt', token, { httpOnly: true })

        return res.json({
            success: true,
            message: 'Successfully logged in.'
        })
    })(req, res, next)
})

router.get('/logout', (req, res) => {
    res.clearCookie('jwt')
    res.redirect('/')
})

router.get('/create', ensureAuthed, (req, res) => {
    return res.render('create', { isLoggedIn: true })
})

router.post('/create', ensureAuthed, async (req, res, next) => {
    const user = await User.findById(req.user.userId)

    let { contents } = req.body
    if(!contents || contents.length > 200) {
        return next({ message: 'Invalid contents' })
    }
    contents = contents.toString()

    try {
        const noteId = Math.floor(Math.random() * 10**12)
        const note = new Note({ owner: user._id, noteId, contents })
        await note.save()

        user.notes.push(note._id)
        await user.save()

        return res.json({
            success: true,
            message: 'Note created.'
        })
    } catch {
        return next({ message: 'An error occurred' })
    }
})

router.get('/edit', ensureAuthed, async (req, res) => {
    let q = req.query
    try {
        if('noteId' in q && parseInt(q.noteId) != NaN) {
            const note = await Note.findOne(q)

            if(!note) {
                return res.render('error', { isLoggedIn: true, message: 'Note does not exist!' })
            }

            if(note.owner.toString() != req.user.userId.toString()) {
                return res.render('error', { isLoggedIn: true, message: 'You are not the owner of this note!' })
            }

            res.render('edit', { isLoggedIn: true, noteId: note.noteId, contents: note.contents })
        } else {
            return res.render('error', { isLoggedIn: true, message: 'Invalid request' })
        }
    } catch {
        return res.render('error', { isLoggedIn: true, message: 'Invalid request' })
    }
})

router.post('/edit', ensureAuthed, async (req, res, next) => {
    let q = req.query
    try {
        if('noteId' in q && parseInt(q.noteId) != NaN) {
            const note = await Note.findOne(q)

            if(!note) {
                return next({ message: 'Note does not exist!' })
            }

            if(note.owner.toString() != req.user.userId.toString()) {
                return next({ message: 'You are not the owner of this note!' })
            }

            let { contents } = req.body
            if(!contents || contents.length > 200) {
                return next({ message: 'Invalid contents' })
            }
            contents = contents.toString()
            note.contents = contents
            await note.save()
            return res.json({ success: true, message: 'Note edited.' })
        } else {
            return next({ message: 'Invalid request' })
        }
    } catch(e) {
        return next({ message: 'Invalid request' })
    }
})

router.use((err, req, res, next) => {
    res.status(err.status || 400).json({
        success: false,
        error: err.message || 'Invalid Request',
    })
})

module.exports = router
