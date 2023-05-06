const express = require("express")
const cookieParser = require("cookie-parser")
const ejs = require("ejs")
require("dotenv").config()

const app = express()
app.use(express.urlencoded({ extended: true }))
app.use(cookieParser())
app.set("view engine", "ejs")
app.use(express.static("public"))

const users = [
    {
        userID: "972",
        username: "kupatergent",
        password: "gandal"
    },
    {
        userID: "***",
        username: "admin"
    }
]

app.get("/", (req, res) => {
    const admin = users.find(u => u.username === "admin")
    if(req.cookies && req.cookies.userData && req.cookies.userData.userID) {
        const {userID, username} = req.cookies.userData
        if(req.cookies.userData.userID === admin.userID) res.render("home.ejs", {username: username, flag: process.env.FLAG})
        else res.render("home.ejs", {username: username, flag: "no flag for you"})
    } else {
        res.render("unauth.ejs")
    }
})

app.route("/login")
.get((req, res) => {
    if(req.cookies.userData && req.cookies.userData.userID) {
        res.redirect("/")
    } else {
        res.render("login.ejs", {err: false})
    }
})
.post((req, res)=> {
    const request = {
        username: req.body.username,
        password: req.body.password
    }
    const user = users.find(u => (u.username === request.username && u.password === request.password))
    if(user) {
        res.cookie("userData", {userID: user.userID, username: user.username})
        res.redirect("/")
    } else {
        res.render("login", {err: true}) // didn't work!
    }
})

app.get("/logout", (req, res) => {
    res.clearCookie("userData")
    res.redirect("/login")
}) 

app.listen(3000, (err) => {
    if (err) console.log(err);
    else console.log("connected at 3000 :)");
})