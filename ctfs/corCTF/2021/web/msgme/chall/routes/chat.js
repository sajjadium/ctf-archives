const express = require("express");
const router = express.Router();

const ws = require("../src/ws.js");

const requiresLogin = (req, res, next) => {
    if(!req.session.user) {
        return res.redirect("/chat/");
    }
    next();
};

router.get("/", (req, res) => {
    res.render("chat");
});

router.post('/login', async (req, res) => {
    let { name } = req.body;
    if(name) {
        if(!['admin', 'system'].includes(name) && !ws.getUser(name)) {
            req.session.user = name;
            return res.json({ success: true });
        }
    }
    return res.json({ success: false });
});

router.post('/admin_login', async (req, res) => {
    let { password } = req.body;
    if(password && password === process.env.ADMIN_PASSWORD) {
        req.session.user = "admin";
        req.session.admin = true;
        return res.json({ success: true });
    }
    return res.json({ success: false });
});

router.post("/send", requiresLogin, (req, res) => {
    let { to, msg } = req.body;
    if(!to || !msg) {
        return res.json({ success: false });
    }

    ws.sendMessage(req.session.user, to, msg);
    return res.json({ success: true });
});

router.get("/logout", (req, res) => {
    req.session.destroy();
    res.redirect("/");
});

router.ws("/ws", (ws, req) => {
    if(!req.session.user) return;
    if(req.headers.origin !== process.env.SITE) {
        console.log(`invalid origin ${req.headers.origin}, expected ${process.env.SITE}`);
        return;
    }
    ws.user = req.session.user;
    ws.admin = req.session.admin;
});

module.exports = router;