"use strict";
const express = require("express");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const typeorm_1 = require("typeorm");
const User_1 = require("../entity/User");
const data = require('../../projectconfig.json');
const saltRounds = 5;
const secret = data["jwt-secret"];
var corsOptions = {
    origin: true,
    credentials: true
};
let router = express.Router();
router.post("/users", async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    bcrypt.hash(req.body.password, saltRounds, async (err, hash) => {
        try {
            req.body.password = hash;
            req.body.images = "";
            const user = userRepository.create(req.body);
            var results = await userRepository.save(user);
            var token = jwt.sign({ id: results["id"], "name": results["name"] }, secret);
            res.cookie('token', token, { sameSite: 'none', secure: true, domain: ".r41k0u.me" });
            return res.status(200).send({ "token": token });
        }
        catch (err) {
            return res.send(400);
        }
    });
});
router.post("/login", async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    const user = await userRepository.findOne({ email: req.body.email });
    if (user) {
        bcrypt.compare(req.body.password, user.password, (err, result) => {
            if (result == true) {
                var token = jwt.sign({ id: user.id, "name": user.name }, secret);
                res.cookie('token', token, { secure: true });
                return res.status(200).send({ "token": token });
            }
            else {
                return res.status(401).send("Invalid Password");
            }
        });
    }
    else {
        return res.status(401).send("Invalid Email");
    }
});
router.options('/region', cors(corsOptions));
router.post("/region", cors(corsOptions), async function (req, res) {
    res.cookie('regionURL', req.body.region, { sameSite: 'none', secure: true, domain: ".r41k0u.me" });
    return res.status(200).send("Region Set");
});
module.exports = router;
