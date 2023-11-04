const express = require('express');
const crypto = require('crypto');
const db = require('../utils/db');
const generateUsername = require('../utils/usernameGenerator');
const router = express.Router();
const botChallenge = require('../utils/report');
const rateLimit = require('express-rate-limit')

premiumPin = process.env.PREMIUM_PIN ? process.env.PREMIUM_PIN : '123-456-012' // remote is different numbers but same format ([0-9]{3}-[0-9]{3}-[0-9]{3}). Please don't try to brainless brute the 1 billion possibilities (if you try do so anyway there will be consequences >:D )

router.get('/', async (req, res) => {
    user = await db.getUserBy("token", req.cookies?.token)
    if (user) {
         isPremium = user.isPremium
        username = user.username
        return res.render('home',{username, isPremium});
    } else {
        res.render('index');
    }
});

router.get('/register', async (req, res) => {
    token  = crypto.randomBytes(16).toString('hex');
    username = generateUsername()
    while (await db.getUserBy("username", username)) //fuck you birthday paradox
      username = generateUsername()
    while (await db.getUserBy("token", token)) //see above
      token = crypto.randomBytes(16).toString('hex');
    await db.registerUser(username, token);
    res.setHeader('Set-Cookie',`token=${token}`);
    return res.render('welcome', {username, token});
});

router.get('/settings', (req, res) => {
    res.render('settings');
});

router.get('/login', (req, res) => {
    res.render('login');
});

router.post('/login', async (req, res) => {
    if (! req.body["token"]) return res.status(401).json('no');
    token = req.body["token"].toString()
    if (await db.getUserBy("token", token)) {
        res.setHeader('Set-Cookie',`token=${token}`);
        return res.status(200).json('yes ok');
    } else {
        return res.status(401).json('no');
    }
});

router.post('/updateUser', async (req, res) => {
    token = req.cookies["token"]
    if (token) {
        user = await db.getUserBy("token", token)
        if (user) {
            enteredPremiumPin = req.body["premiumPin"]
            if (enteredPremiumPin) {
                enteredPremiumPin = enteredPremiumPin.toString()
                if (enteredPremiumPin == premiumPin) {
                    user.isPremium = 1
                } else {
                    return res.status(401).json('wrong premium pin');
                }
            }
            if (req.body["username"]) {
                exists = await db.getUserBy("username", req.body["username"].toString())
                if (exists) return res.status(401).json('username taken');
                username = req.body["username"].toString()
                if (username.length > 4096) return res.status(401).json('username too long');
                user.username = username
            }
            await db.updateUserByToken(token, user)
            return res.status(200).json('yes ok');
        }
    }
    return res.status(401).json('no');
});

router.post('/createChallenge', async (req, res) => {
    token = req.cookies["token"]
    if (token) {
        user = await db.getUserBy("token", token)
        if (user && req.body["longitude"] && req.body["latitude"] && req.body["img"]) {
            chalId = crypto.randomBytes(16).toString('hex')
            if (user.isPremium) {
                if ((!req.body["winText"]) || (!req.body["OpenLayersVersion"])) return res.status(401).json('huh');
                winText = req.body["winText"].toString()
                OpenLayersVersion = req.body["OpenLayersVersion"].toString()
            } else {
                winText = "Well played! :D"
                OpenLayersVersion = "2.13"
            }
            await db.createChallenge(chalId, user.token, req.body["longitude"].toString(), req.body["latitude"].toString(), req.body["img"].toString(), OpenLayersVersion, winText)
            return res.status(200).json(chalId);
        }
    }
    return res.status(401).json('no');
});



router.post('/challengeUser', async (req, res) => {
    token = req.cookies["token"]
    if (token) {
        user = await db.getUserBy("token", token)
        if (user && req.body["username"] && req.body["duelID"]) {
            console.log(req.body["username"].toString())
            targetUser = await db.getUserBy("username", req.body["username"].toString())
            console.log(targetUser)
            if (!targetUser) return res.status(401).json('who dis?');
            chall = await db.getChallengeById(req.body["duelID"].toString())
            if (!chall) return res.status(401).json('huh?');
            db.addNotificationToUserToken(targetUser.token, `${user.username} has challenged you to a game! <a href="/challenge?id=${chall.id}">Click here to play!</a>`)
            return res.status(200).json('yes ok');
        }
    }
    return res.status(401).json('no');
});

sanitizeHTML = (input) => input.replaceAll("<","&lt;").replaceAll(">","&gt;")

router.get('/challenge', async (req, res) => {
    if (!req.query.id) return res.status(404).json('wher id');
    chall = await db.getChallengeById(req.query.id.toString())
    if (!chall) return res.status(404).json('no');
    libVersion = chall.OpenLayersVersion
    img = chall.image
    challId = chall.id
    iframeAttributes = "sandbox=\"allow-scripts allow-same-origin\" " // don't trust third party libs
    iframeAttributes += "src=\"/sandboxedChallenge?ver="+sanitizeHTML(libVersion)+"\" "
    iframeAttributes += "width=\"70%\" height=\"97%\" "
    res.render('challenge', {img, challId, iframeAttributes});
});

router.get('/sandboxedChallenge', async (req, res) => {
    if (!req.query.ver) return res.status(404).json("wher ver");
    res.render('sandboxedChallenge', {libVersion: req.query.ver.toString()});
});

router.post('/solveChallenge', async (req, res) => {
    if (!req.body["challId"]) return res.status(404).json("bruh");
    chall = await db.getChallengeById(req.body["challId"].toString())
    if (!chall) return res.status(401).json('huh?');
    Math.sqrt((parseFloat(chall.longitude) - parseFloat(req.body.longitude.toString()))**2
    + (parseFloat(chall.latitude) - parseFloat(req.body.latitude.toString()))**2) < 0.001 ?
    res.status(200).json(chall.winText) : res.status(401).json('no');
});

const limiter = rateLimit.rateLimit({
        windowMs: 1 * 60 * 1000, // 1 minute
        max: 2, // Limit each IP to 100 requests per `window` (here, per 1 minute)
        standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
        legacyHeaders: false, // Disable the `X-RateLimit-*` headers
}) // please don't exhaut all resources 🥺 👉👈



router.get("/bot", limiter, async (req, res) => {
    if (!req.query.username) return res.status(404).json('what are you even doing lol')
    botChallenge(req.query.username.toString(),premiumPin)
    return res.status(200).json('successfully received :)');
});

module.exports = () => {
    return router;
}
