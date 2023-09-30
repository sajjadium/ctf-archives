const express = require("express");
const path = require("path");
const router = express.Router();
const util = require('../util');

router.get('/register', (req, res) => {
    return res.sendFile(path.join(__dirname, '../public/register.html'));
});

router.post('/register', async (req, res) => {
    var obj = {};
    for (const k in req.body) {
        if (k.toLowerCase() == "username" && req.body[k].toLowerCase() == "admin") {
            return res.status(400).send("You can't use that username.");
        };
        obj[k.toLowerCase()] = req.body[k];
        
    }

    if (!obj["password"] || !obj["username"]) {
        return res.status(400).send("Invalid body.");
    }

    console.log(obj);
    console.log(obj.username);
    console.log(JSON.stringify(obj));
    try {
        await util.db.insert_response(obj.username, obj.password);

        return res.redirect('/user/login');
    } catch {
        return res.status(500).send("An error occurred with processing!");
    }
});

router.get('/login', (req, res) => {
    return res.sendFile(path.join(__dirname, '../public/login.html'));
});


router.post('/login', async (req, res) => {
    const {username, password} = req.body;

    try {
       const real_password = await util.db.read_response(username);
       if (real_password) {
        if (real_password !== password) {
            return res.status(400).send("invalid credentials");
        }
        
        req.session.user = username;
        return res.redirect('/joi');
       }
    } catch {
        return res.status(500).send("An error occurred with processing!");
    }

});

module.exports = router;
