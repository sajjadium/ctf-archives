const express = require('express')
const router = express.Router()
const User = require('../models/User')

// add Admin
User.findOneAndUpdate({
        username: 'admin'
    }, 
    {
        $setOnInsert: {
            password: process.env.ADMIN_PASS
        }
    }, 
    {
        upsert: true,
        new: true
    })
    .then(console.log('[+] Admin added'))
    .catch(err => console.log(err))


// login page
router.get('/login', async (req, res) => {
    return res.render('login')
})

//logout page
router.get('/logout', (req, res) => {
    req.session.username = ''
    req.flash('success', 'Logged out successfully.')
    return res.redirect('/user/login')
})

// register
router.get('/register', (req, res) => {
    return res.render('register')
})

// register post
router.post('/register', async(req, res) => {
    let { username, password, password2  } = req.body
    let errors = []
    // check it
    if(!username || !password || !password2){
        errors.push({ msg: 'Please fill in all fields.'})
    }
    if(password !== password2){
        errors.push({ msg: 'Password do not match.'})
    }
    if(password.length < 4){
        errors.push({ msg: 'Password must be at least 4 characters.'})
    }
    if(username.length < 4){
        errors.push({ msg: 'Username must be at least 4 characters.'})
    }

    let user = await User.findOne({username: username})
    if(user){
        errors.push({ msg: 'Username is already taken.'})
    }

    if(errors.length){
        return res.render('register', {
            errors,
            username,
            password,
            password2
        })
    }
    else {
        const newUser = new User({
            username,
            password
        })
        newUser.save()
            .then(user => {
                req.flash('success', 'You are now registered.')
                return res.redirect('/user/login')
            })
            .catch(err => {
                req.flash('success', 'DB error LOL.')
                console.log(err)
                return res.redirect('/user/login')
            })
    }
})

// login post
router.post('/login', (req, res) => {
    let { username, password  } = req.body
    User.findOne({username: username})
        .then(user => {
            if(!user){
                return res.render('login', {
                    errors: [{ msg: 'Username does not exit.'}],
                    username,
                    password,
                })
            }
            else if(user.password !== password){
                return res.render('login', {
                    errors: [{ msg: 'Password or Username not correct.'}],
                    username,
                    password,
                })
            }
            else{
                req.session.username = user.username
                return res.redirect('/')

            }
        })
})


module.exports = router


