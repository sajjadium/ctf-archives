const express = require("express");

const multer = require("multer");
const { v4: uuidv4 } = require('uuid');

const fsp = require("fs/promises");

const upload = multer({
    limits: {
        fileSize: 500000 // 500 kB
    },
    storage: multer.diskStorage({
        destination: './uploads/',
        filename: (req, file, cb) => {
            cb(null, uuidv4() + ".mp3");
        }
    })
});

const utils = require("../src/utils.js");
const db = require("../src/db.js");
const jwt = require("../src/jwt.js");

const router = express.Router();

const requiresLogin = (req, res, next) => {
    if(!req.user || !db.hasUser(req.user.username)) {
        return res.redirect("/");
    }
    next();
};

router.use((req, res, next) => {
    res.setHeader("Cache-Control", "no-store, no-cache");
    next();
});

router.post("/login", async (req, res) => {
    let { username, password } = req.body;

    if(!db.hasUser(username)) {
        utils.alert(req, res, "danger", `No user found with username ${username}`);
        return res.redirect("/");
    }

    if(!await db.checkLogin(username, password)) {
        utils.alert(req, res, "danger", `Incorrect password`);
        return res.redirect("/");
    }

    jwt.signData(res, username, { msg: "Logged in successfully", type: "primary" });
    res.redirect("/home");
});

router.post("/register", async (req, res) => {
    let { username, password } = req.body;

    if(db.hasUser(username)) {
        utils.alert(req, res, "danger", `A user already exists with username ${username}`);
        return res.redirect("/");
    }

    if(username.length > 16) {
        utils.alert(req, res, "danger", "Invalid username");
        return res.redirect("/");
    }
    if(password.length < 5) {
        utils.alert(req, res, "danger", "Please choose a longer password");
        return res.redirect("/");
    }

    await db.addUser(username, password);

    jwt.signData(res, username, { msg: "Registered successfully", type: "primary" });
    res.redirect("/home");
});

router.post("/logout", (req, res) => {
    res.clearCookie("session");
    res.redirect("/");
});

router.get("/alerts/list", (req, res) => {
    let data = req.user?.alert;
    jwt.signData(res, req.user?.username, null);
    utils.jsonp(req, res, "alerts", data);
});

router.get("/user/info", requiresLogin, (req, res) => {
    utils.jsonp(req, res, "user", req.user.username);
});

router.get("/notes/list", requiresLogin, (req, res) => {
    utils.jsonp(req, res, "notes", db.getNotes(req.user.username));
});

router.get("/audio/file", requiresLogin, async (req, res) => {
    if(!db.getMemo(req.user.username)) {
        return res.status(404).send('no');
    }
    if(req.header('Sec-Fetch-Dest') !== "audio" || req.header('Sec-Fetch-Site') !== "same-origin") {
        return res.status(404).send('no');
    }

    res.setHeader('content-type', 'audio/mpeg');
    res.sendFile(db.getMemo(req.user.username), { root: "." });
});

router.use((req, res, next) => {
    if(req.user && req.user.username === "admin") {
        // what are you trying to do to my challenge??? :<
        return res.redirect("/home");
    }
    next();
});

router.post("/notes/add", requiresLogin, (req, res) => {
    let { note } = req.body;
    if(!note) {
        utils.alert(req, res, "danger", `No note was provided`);
        return res.redirect("/home");
    }
    db.addNote(req.user.username, note);
    res.redirect("/home");
});

router.post("/notes/remove", requiresLogin, (req, res) => {
    let { index } = req.body;
    
    index = parseInt(index);
    if(isNaN(index)) {
        utils.alert(req, res, "danger", `Invalid note to remove`);
        return res.redirect("/home");
    }

    db.removeNote(req.user.username, index);
    res.redirect("/home");  
});

router.post("/audio/upload", [requiresLogin, upload.single('audio')], async (req, res) => {
    if(!req.file) {
        return res.redirect("/home");
    }
    
    let { path } = req.file;

    if(db.getMemo(req.user.username)) {
        try { await fsp.rm(db.getMemo(req.user.username)); } catch {}
    }

    db.setMemo(req.user.username, path);

    utils.alert(req, res, "primary", `Voice memo uploaded successfully`);
    res.redirect("/home");
});

router.post("/audio/remove", requiresLogin, async (req, res) => {
    if(db.getMemo(req.user.username)) {
        try { await fsp.rm(db.getMemo(req.user.username)); } catch {}
    }

    db.setMemo(req.user.username, null);
    utils.alert(req, res, "primary", `Voice memo removed successfully`);
    res.redirect("/home");
});

module.exports = router;