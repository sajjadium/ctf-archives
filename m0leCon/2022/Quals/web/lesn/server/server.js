const express = require('express')
const uuid = require('uuid')
const sqlite3 = require('sqlite3')
const cookieParser = require('cookie-parser')
const jwt = require('jsonwebtoken')
const fetch = require('cross-fetch')
const { open } = require('sqlite')
const { sanitize } = require('./sanitize')
require('express-async-errors')

const app = express()
const port = 3000

app.set('view engine', 'ejs')
app.use(express.urlencoded({ extended: false }))
app.use('/static', express.static('public', { maxAge: 3600000 }))
app.use(cookieParser())

const JWT_SECRET_KEY = uuid.v4()
const ADMIN_PWD = process.env.ADMIN_PWD || 'REDACTED'
const FLAG = process.env.FLAG || 'ptm{REDACTED}'
const WEBAPP_URL = process.env.WEBAPP_URL
const BOT_URL = process.env.BOT_URL
const RECAPTCHA_SECRET_KEY = process.env.RECAPTCHA_SECRET_KEY

let db = undefined;

(async () => {
    // open the database
    db = await open({
        filename: ':memory:',
        driver: sqlite3.Database
    })
})().then(async () => {
    await db.exec('CREATE TABLE posts (id VARCHAR(36), user VARCHAR (40), description TEXT, imgurl TEXT, PRIMARY KEY(id))')
    await db.run('INSERT INTO posts (id, user, description, imgurl) VALUES (?,?,?,?)', [uuid.v4(), 'admin', FLAG, 'https://ptmd.m0lecon.it/img/pwnthem0le_logo.png'])
})



app.get('/admin', async (req, res) => {
    res.render('admin')
})

app.post('/admin', async (req, res) => {
    const pwd = req.body.password
    if (ADMIN_PWD && ADMIN_PWD === pwd) {
        res.cookie('session', jwt.sign({ user: 'admin' }, JWT_SECRET_KEY), { secure: true, httpOnly: true, sameSite: 'none' })
        return res.redirect('/')
    }
    return res.status(400).render('400', { from: '/admin', error: 'Wrong password' })
})

app.use((req, res, next) => {
    if (req.cookies.session) {
        try {
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET_KEY)
            if (decoded && decoded.user) {
                res.locals.loggedUser = decoded.user
            }
        } catch (err) {

        }
    }

    if (!res.locals.loggedUser) {
        const user = uuid.v4()
        res.locals.loggedUser = user
        res.cookie('session', jwt.sign({ user: user }, JWT_SECRET_KEY), { secure: true, httpOnly: true, sameSite: 'none' })
    }

    next()
})



app.get('/', async (req, res) => {
    const error = req.query.err

    res.render('index', { error })
})

app.get('/post', async (req, res) => {
    const posts = await db.all('SELECT id FROM posts WHERE user = ?', [res.locals.loggedUser])
    res.render('post_list', { posts })
})

app.get('/post/:id', async (req, res) => {
    const imgid = req.params.id
    const post = await db.get('SELECT * FROM posts WHERE id = ?', [imgid])

    if (!post) {
        return res.status(404).render('404')
    }

    res.render('post', { imgurl: post.imgurl, description: post?.description, imgid })

})

app.get('/new', async (req, res) => {
    res.render('new')
})

app.post('/new', async (req, res) => {
    const description = req.body.description
    const imgurl = req.body.imgurl

    if (!description || typeof description !== 'string' || !imgurl || typeof imgurl !== 'string' || !/^https?:\/\/.+$/.test(imgurl) || res.locals.loggedUser === 'admin') {
        return res.status(400).render('400', { from: '/new', error: undefined })
    }

    const imgid = uuid.v4()

    const clean = sanitize(description)


    db.run('INSERT INTO posts (id, description, imgurl, user) VALUES (?,?,?,?)', [imgid, clean, imgurl, res.locals.loggedUser])

    return res.redirect('/post/' + imgid)
})

app.get('/edit/:id', async (req, res) => {
    const imgid = req.params.id
    const post = await db.get('SELECT * FROM posts WHERE id = ?', [imgid])

    if (!post) {
        return res.status(404).render('404')
    }

    const error = req.query.err

    res.render('edit', { imgurl: post.imgurl, description: post.description, imgid, error })

})


app.post('/edit/:id', async (req, res) => {
    const imgid = req.params.id
    const post = await db.get('SELECT * FROM posts WHERE id = ?', [imgid])

    if (!post) {
        return res.status(404).render('404')
    }

    const description = req.body.description
    const imgurl = req.body.imgurl

    if (!description || typeof description !== 'string' || !imgurl || typeof imgurl !== 'string' || !/^https?:\/\/.+$/.test(imgurl) || res.locals.loggedUser === 'admin') {
        return res.status(400).render('400', { from: '/edit/' + imgid, error: undefined })
    }

    const clean = sanitize(description)


    db.run('UPDATE posts SET description = ?, imgurl = ? WHERE id = ?', [clean, imgurl, imgid])

    return res.redirect('/post/' + imgid)

})

app.get('/report', async (req, res) => {
    res.render('report', { error: undefined, success: undefined })
})


app.post('/report', async (req, res) => {
    const url = req.body.url
    const re = new RegExp(`${WEBAPP_URL}/post/.*`);

    if (!url || !re.test(url)) {
        return res.status(400).render('report', { error: 'Bad url, must start with : ' + WEBAPP_URL + '/post/', success: undefined })
    }


    if (RECAPTCHA_SECRET_KEY) {
        const captchaToken = req.body['g-recaptcha-response']

        if (!captchaToken || typeof captchaToken !== 'string') {
            return res.status(400).render('report', { error: 'Bad captcha', success: undefined })
        }

        const sp = new URLSearchParams({ "secret": RECAPTCHA_SECRET_KEY, "response": captchaToken })
        const url_captcha = 'https://www.google.com/recaptcha/api/siteverify?' + sp

        // Making POST request to verify captcha
        try {
            captchaVerified = await fetch(url_captcha, {
                method: "post",
            })
                .then((response) => response.json())
                .then((google_response) => {
                    console.log(google_response)
                    if (google_response.success === true) {
                        //   if captcha is verified
                        return true;
                    } else {
                        // if captcha is not verified
                        return false;
                    }
                })

            //console.log(captchaVerified)
            if (!captchaVerified) {
                return res.status(400).render('report', { error: 'Invalid captcha', success: undefined })
            }

        } catch (e) {
            console.log(e)
            return res.status(500).render('report', { error: 'Impossible verify captcha, contact an admin', success: undefined })
        }
    }


    try {
        const r = await fetch(BOT_URL, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        }).then(r => r.text())
        console.log(r)
    } catch (error) {
        return res.status(500).render('report', { error: 'Error: ' + error, success: undefined })
    }

    return res.render('report', { error: undefined, success: 'An admin checked your post!' })
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})