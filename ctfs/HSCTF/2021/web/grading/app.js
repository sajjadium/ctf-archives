require("dotenv").config()

const express = require("express")
const ejs = require("ejs")
const mongoose = require("mongoose");
const passport = require("passport");
const passportLocalMongoose = require("passport-local-mongoose");
const session = require('express-session');
const MongoStore = require("connect-mongo")

const app = express()

app.set("view engine", "ejs")
app.use(express.urlencoded({extended: true}))
app.use(express.static("public"))

mongoose.connect(process.env.MONGO || "mongodb://localhost:27017/grading1DB", {useNewUrlParser: true})

const questionSchema = new mongoose.Schema({
    question: String,
    choices: [String],
    answer: String,
    submission: String
})

const userSchema = new mongoose.Schema({
    username: String,
    password: String,
    forms: [new mongoose.Schema({
        questions: [{type: mongoose.Schema.Types.ObjectID}],
        name: String,
        deadline: Date,
        submitted: Boolean,
    })],
    questions: [questionSchema],
})

userSchema.plugin(passportLocalMongoose)

const User = new mongoose.model("user", userSchema)

// passport-local-mongoose shortcut
passport.use(User.createStrategy())

app.use(session({
    secret: process.env.SESSION_SECRET || "welp_here_we_are",
    resave: false,
    saveUninitialized: false,
    store: MongoStore.create({
        mongoUrl: process.env.MONGO || "mongodb://localhost:27017/grading1DB"
    })
}))

app.use(passport.initialize())
app.use(passport.session())

passport.serializeUser((user, done) => {
    done(null, user.id)
})

passport.deserializeUser((userDataFromCookie, done) => {
    User.findById(userDataFromCookie, (err, user) => {
        done(err, user)
    })
})


// routing

const authMW = (req, res, next) => {
    if(req.isAuthenticated()) {
        next()
    } else res.redirect("/login")
}

// auth
app.route("/login")
.get((req, res) => {
    if(!req.isAuthenticated()) {
        res.render("login.ejs", {err: null})
    } else res.redirect("/")
})
.post(passport.authenticate('local', { successRedirect: '/',
failureRedirect: '/login' }))

app.route("/register")
.get((req, res) => {
    res.render("register.ejs", {err: null})
})
.post((req, res) => {
    User.register({username: req.body.username}, req.body.password, (err, user) => {
        if(err) {
            console.log(err);
            res.render("register.ejs", {err: err})
        } else {
            const question1 = {
                question: "What is the capital of Africa?",
                choices: [
                    "Venezuela",
                    "Kalibloom",
                    "Nairobi",
                    "Tokyo",
                    "Africa is not a country"
                ],
                answer: "Africa is not a country",
                submission: "Kalibloom",
            }

            const question2 = {
                question: "What is the best CTF?",
                answer: "HSCTF",
            }

            user.questions.push(question1)
            user.questions.push(question2)
            user.save()

            console.log(user.questions);

            const failedTest = {
                name: "simple quiz",
                questions: [
                    user.questions[0]._id,
                ],
                deadline: new Date(2021, 5, 13, 0, 0, 0)
            }
            
            const newTest = {
                name: "another simple quiz",
                questions: [
                    user.questions[1]._id,
                ],
                deadline: new Date(2021, 5, 19, 0, 0, 0)
            }

            user.forms.push(failedTest)
            user.forms.push(newTest)
            user.save()

            passport.authenticate("local")(req, res, () => {
                res.redirect("/")
            })
        }
    })
})

app.get("/logout", (req, res) => {
    req.logout()
    res.redirect("/")
})

// actual routes
app.get("/", authMW, (req, res) => {
    // console.log(req.user);
    res.render("home.ejs", {forms: req.user.forms, user: req.user.username})
})

app.route("/:formID")
.get(authMW, (req, res) => {
    const formID = req.params.formID
    const form = req.user.forms.id(formID)
    if(!form) {
        res.redirect("/") // not found
    } else {

        const payload = {
            name: form.name,
            deadline: form.deadline,
            questions: []
        }

        for(let q in form.questions) {
            form.questions[q] = req.user.questions.id(form.questions[q])
        }

        after = {}

        const late = Date.now() > form.deadline
        after.late = late

        if(late) {
            let grade = 0
            for(let q of form.questions) {
                if (q.submission == q.answer) grade += 1
            }

            after.grade = grade
        }

        after.flag = process.env.FLAG

        // console.log(form, form.questions[0]);
        res.render("form.ejs", {form: form, after: after})
    }
})
.post(authMW, (req, res) => {
    const now = Date.now()
    const form = req.user.forms.id(req.params.formID)
    if(now > form.deadline) {
        res.json({response: "too late"})
    } else {
        if(req.body.ID) {
            const question = req.user.questions.id(req.body.ID)
            console.log(question);
            question.submission = req.body.value
            req.user.save()
        } else {
            form.submitted = true
            req.user.save()
        }

        res.json({response: "heh"})
    }

})



app.listen(process.env.PORT || 3000, (err) => {
    if(!err) console.log("connected on 3000 :)");
    else console.log(err);
})