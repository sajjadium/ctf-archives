const { Mongoose } = require('mongoose');
const bcrypt = require("bcrypt");
const connectDB = require('../database/connection');
var UserCol = require('../model/model');
const session = require('express-session');
const jwt = require('jsonwebtoken')
require('dotenv').config()

//const store = new session.MemoryStore();

exports.login = (req, res) => {
    if (!req.body) {
        res.status(400).send({ message: "Content can not be empty!" });
        return;
    }

    if (!req.body.username) {
        res.status(400).send({ message: "Username can not be empty!" });
        return;
    }

    if (!req.body.password) {
        res.status(400).send({ message: "Password can not be empty!" });
        return;
    }

    const username = req.body.username;

    UserCol.findOne({ Username: req.body.username }).maxTimeMS(100).then(user => {
        if (user) {
            bcrypt
                .compare(req.body.password, user.Password, function (err, result) {
                    if (result) {
                        const user = {
                            name: username,
                            authorized: true,
                            admin: false
                        }
                        const accessToken = generateAccessToken(user)
                        req.session.username = username

                        res.cookie("token", accessToken, "user", user, {
                            httpOnly: true,
                        });
                        res.render("dashboard", { name: username })
                    } else {
                        res.status(500).send({ message: "Password incorrect" })
                    }
                });
        } else {
            res.render('index', { error: "User not found" })
        }
    }).catch(err => {
        res.status(500).send({ message: "Error occured" })
    })
}

exports.register = (req, res) => {
    if (!req.body) {
        res.status(400).send({ message: "Content can not be empty!" });
    }

    if (!req.body.username) {
        res.status(400).send({ message: "Username can not be empty!" });
        return;
    }

    if (!req.body.password) {
        res.status(400).send({ message: "Password can not be empty!" });
        return;
    }
    // Check if User Exists 
    UserCol.findOne({ Username: req.body.username }).then(user => {
        if (user) {
            res.status(500).send({ message: "Username exists" })
        }
    }).catch(err => {
        res.status(500).send({ message: err.message || "Error occured" })
    })

    const password = req.body.password;
    const username = req.body.username;
    const email = req.body.email;
    const saltRounds = 10;

    bcrypt
        .genSalt(saltRounds,)
        .then(salt => {
            console.log('Salt: ', salt)
            return bcrypt.hash(password, salt)
        })
        .then(hash => {
            const user = new UserCol({
                Email: email,
                Username: username,
                Password: hash
            });
            user.save(user)
                .catch(err => {
                    res.status(500).send({ message: err.message || "Error occured" })
                })
            res.render('index')
        })
        .catch(err => console.error(err.message))
}

exports.logout = (req, res) => {
    res.clearCookie('token')
    res.render('index')
}

function generateAccessToken(user) {
    return jwt.sign(user, process.env.SECRET)
}
