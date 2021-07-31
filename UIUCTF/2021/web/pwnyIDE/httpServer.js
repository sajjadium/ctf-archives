import express from "express"
import hcaptcha from "hcaptcha"
import multer from "multer"
import Joi from "joi"
import ejv from "express-joi-validation"
const validator = ejv.createValidator({})
import { randomBytes } from "crypto"
import fs from "fs"
import cookieParser from "cookie-parser"
import { execFile } from "child_process"
import { Users } from "./index.js"

const app = express()
app.use(express.urlencoded({ extended: false }))
app.use(cookieParser(randomBytes(64).toString("hex")))
app.use(express.static("static"))

const upload = multer({
    storage: multer.diskStorage({
        destination: (req, _file, cb) => {
            if (req.signedCookies.uid)
                cb(null, `/files/${req.signedCookies.uid}/`)
            else
                cb("Not signed in")
        },
        filename: (_req, _file, cb) => cb(null, "file")
    }),
    limits: {
        files: 1,
        parts: 1,
        fields: 0,
        fileSize: 1024 * 1024 // 1MB
    }
})

app.get(
    "/", 
    (req, res) => {
        if (req.signedCookies.uid)
            res.redirect("/app.html")
        else
            res.redirect("/login.html")
    })

app.post(
    "/register",
    validator.body(Joi.object({
        username: Joi.string().alphanum().min(5).max(20).required(),
        password: Joi.string().min(8).max(50).required()
    })),
    (req, res) => {
        if (Users.get(req.body.username)) {
            res.status(400)
            res.send("That user already exists")
            return
        }
        const uid = randomBytes(16).toString("hex")
        fs.mkdirSync(`/files/${uid}/`)
        Users.set(req.body.username, {
            username: req.body.username,
            password: req.body.password,
            uid: uid
        })
        res.cookie("uid", uid, { signed: true })
        res.redirect("/app.html")
    })

app.post(
    "/login",
    validator.body(Joi.object({
        username: Joi.string().required(),
        password: Joi.string().required()
    })),
    (req, res) => {
        const user = Users.get(req.body.username)
        if (!user) {
            res.status(401)
            res.send("Invalid credentials")
            return
        }
        res.cookie('uid', user.uid, { signed: true })
        res.redirect("/app.html")
    })

app.post(
    "/save", 
    upload.single("file"), 
    (req, res) => {
        if (!req.signedCookies.uid) {
            res.status(401)
            res.send("Not logged in")
            return
        }
        res.send("Saved")
    })

app.get(
    "/workspace/:uid", 
    validator.params(Joi.object({
        uid: Joi.string().regex(/^[a-f0-9]{32}$/)
    })),
    (req, res) => {
        res.setHeader("Content-Security-Policy", "sandbox")
        res.setHeader("Content-Type", "text/html; charset=UTF-8")
        if (!fs.existsSync(`/files/${req.params.uid}/file`)) {
            res.send(`<html>\n<head>\n  <title>Test</title>\n</head>\n<body>\n  <div>\n    Hello World\n  </div>\n</body>\n</html>`)
            return
        }
        const data = fs.readFileSync(`/files/${req.params.uid}/file`)
        res.send(data)
    })

app.post(
    "/report",
    validator.body(Joi.object({
        url: Joi.string().required(),
        "h-captcha-response": process.env.DEBUG ? Joi.string().optional().allow("") : Joi.string().required(),
        "g-recaptcha-response": process.env.DEBUG ? Joi.string().optional().allow("") : Joi.string().required(),
    })),
    async (req, res) => {
        if (!process.env.DEBUG && req.header("X-ADMIN-TOKEN") !== process.env.ADMIN_TOKEN) {
            if (!/^https?:\/\/pwnyide.chal.uiuc.tf\/workspace\/[a-f0-9]{32}$/.test(req.body.url)) {
                res.status(400)
                res.send("Invalid URL")
                return
            }
            const valid = (await hcaptcha.verify(process.env.HCAPTCHA_SECRET, req.body["h-captcha-response"])).success
            if (!valid) {
                res.status(400)
                res.send("Invalid hCaptcha token")
                return
            }
        }

        // run admin bot
        console.log(`running admin bot for url ${req.body.url}`)
        execFile("node", ["bot.js", req.body.url], (err, _stdout, _stderr) => {console.error(err)})
        res.send("Thanks for your report. An admin will check it out shortly!")
    })

app.get(
    "/ssrf", 
    async (req, res) => {
        res.setHeader("Content-Type", "text/plain; charset=UTF-8")
        if (req.socket.remoteAddress === "127.0.0.1" && req.header("Sec-Pro-Hacker") === "1")
            res.send(process.env.FLAG)
        else
            res.send("glhf ;)")
    })

export default app
