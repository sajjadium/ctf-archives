"use strict";
const express = require("express");
const jwt = require("express-jwt");
const crypto = require("crypto");
const typeorm_1 = require("typeorm");
const User_1 = require("../entity/User");
const moment = require("moment");
const redis_1 = require("redis");
const client = redis_1.createClient();
client.connect();
const data = require('../../projectconfig.json');
let router = express.Router();
const secret = data["jwt-secret"];
router.get("/users/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    const results = await userRepository.findOne(req.user.id);
    return res.send(results);
});
router.put("/users/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    const user = await userRepository.findOne(req.user.id);
    userRepository.merge(user, req.body);
    const results = await userRepository.save(user);
    return res.send(results);
});
router.post("/images/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    const user = await userRepository.findOne(req.user.id);
    const hash = crypto.createHash('sha256');
    hash.update(moment().format());
    const filename = hash.digest('hex');
    console.log(req.files);
    if (req.files && req.files.image) {
        let image = req.files.image;
        let uploadPath = __dirname + '/../images/' + filename + '.jpg';
        image.mv(uploadPath, async function (err) {
            if (err)
                return res.status(500).send(err);
            userRepository.merge(user, { images: user.images + filename + '.jpg,' });
            const results = await userRepository.save(user);
            res.send('File uploaded!');
        });
    }
});
router.get("/images/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req, res) {
    const conn = typeorm_1.getConnection();
    const userRepository = conn.getRepository(User_1.User);
    const user = await userRepository.findOne(req.user.id);
    const images = user.images.split(',');
    images.pop();
    return res.send(images);
});
router.post("/report/", jwt({ secret: secret, algorithms: ['HS256'] }), async function (req, res) {
    console.log(req.body);
    await client.lPush("submissions", req.body.url).then(() => {
        return res.send("Reported");
    });
});
module.exports = router;
