const express = require('express')
const jwt = require('jsonwebtoken')
const crypto = require('crypto')
const cookieParser = require('cookie-parser')
require('express-async-errors')

const FLAG = process.env.FLAG || 'flag{test}'

const app = express()
const port = 3000

app.set('view engine', 'ejs');

const knex = require('knex')({
    client: 'better-sqlite3',
    connection: {
      filename: ":memory:",
    },
    useNullAsDefault: true,
  });
  

const SECRET_KEY = process.env.SECRET_KEY || crypto.randomUUID()

const CHALL_URL = process.env.CHALL_URL || 'http://app.localtest.me:3000'
const SSO_URL = process.env.SSO_URL || 'http://sso.localtest.me:3001'


const SSO_URL_LOGIN = `${SSO_URL}/login?callback=${CHALL_URL}/cb`
const SSO_URL_REGISTER = `${SSO_URL}/register?callback=${CHALL_URL}/registered`
const SSO_CHECK_URL = `${SSO_URL}/check-token`


app.use(cookieParser())
app.use(express.urlencoded({extended: false}))  

app.use((req,res,next)=>{
    res.locals.errormsg = undefined
    res.locals.successmsg = undefined
    next()
})

app.use((req, res, next)=> {
    res.header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline' https://cdn.jsdelivr.net/; style-src 'unsafe-inline' https://cdn.jsdelivr.net/; img-src data: ; connect-src 'self'")
    next()
})


app.use((req, res, next)=> {
    res.locals.loggedUser = undefined
    
    try {
        const decoded = jwt.verify(req.cookies.session, SECRET_KEY)
        //console.log(decoded)
        res.locals.loggedUser = decoded.user
    } catch {

    }
    next()
})


app.get('/login', (req,res) => {
    res.redirect(SSO_URL_LOGIN)
})

app.get('/register', (req,res) => {
    res.redirect(SSO_URL_REGISTER)
})

app.get('/registered', (req,res) => {
    res.locals.successmsg = 'Registered, now you can log in'
    res.render('header')
})

app.get('/cb', async (req,res) => {
    res.render('cb')
})

app.post('/cb', async (req,res) => {
    const token = req.body.token
    console.log(token)

    try {
        if (token && typeof token === 'string'){
            const j = await (await fetch(SSO_CHECK_URL + '?token=' + encodeURIComponent(token))).json()
            console.log(j)
            if (j.user){
                const c = jwt.sign({ user: j.user }, SECRET_KEY);
                res.cookie('session', c)

                const x = await knex('users').where({username: j.user}).first()
                
                if (!x){
                    console.log('Generating profile')
                    await knex('users').insert({username: j.user, desc: 'placeholder', private: true})
                }
                return res.send('ok')
            }
        }
        return res.status(400).send('bad token')
    } catch (e) {
        console.error(e)
        return res.status(500).send('Something is wrong, contact an admin')
    }
    
})

app.get('/', async (req, res) => {
    const users = await knex('users').select('username').where({private: false}).limit(25)
    return res.render('home', {users})
})


app.get('/error', async (req,res) => {
    const msg = req.query.msg || 'Error'
    res.locals.errormsg = msg
    res.render('header')
});


app.get('/profile', async (req, res) => {
    const user = req.query.user

    if (user && typeof user === 'string'){
        const r = await knex.select().from('users').where('username','=',user).first()
        if (r){
            console.log(res.locals.loggedUser)
            if (r.private === 0 || user === res.locals.loggedUser || res.locals.loggedUser === 'admin')
            return res.render('profile', {profile: r})
        } 
    }

    res.locals.errormsg = 'User not found'
    return res.render('header')
});


// check auth
app.use((req, res, next)=> {
    if (!res.locals.loggedUser){
        return res.redirect('/error?msg=Please+log+in')
    }
    next()
});


app.get('/set-profile', async (req, res) => {
    const r = await knex.select().from('users').where('username','=',res.locals.loggedUser).first()
    return res.render('set-profile', {profile: r})
});

app.post('/set-profile', async (req, res) => {

    if (res.locals.loggedUser === 'admin'){
        return res.redirect('/error?msg=Something+is+wrong')
    }
    
    const new_desc = req.body.desc
    const is_private = req.body.private === 'true'
    
    if (! new_desc || typeof new_desc !== 'string'){
        return res.redirect('/error?msg=Bad+description')
    }

    const r = await knex('users')
        .where('username','=',res.locals.loggedUser)
        .update({
            desc: new_desc,
            private: is_private
        })

    res.locals.successmsg = 'Done'
    return res.render('header')
});





(async () => {

    // create empty db
    
    await knex.schema.dropTableIfExists('users')
    
    await knex.schema.createTable('users', function (table) {
        table.string('username',40).primary()
        table.boolean('private')
        table.string('desc')
    })

    await knex('users').insert({username: 'admin', desc: FLAG, private: true})
    await knex('users').insert({username: 'test', desc: '<code id="text" style="color: red">HI</code><script>setInterval(()=>{text.innerText += "I"}, 300)</script>', private: false})

    // start the server
    app.listen(port, () => {
    console.log(`App listening on port ${port}`)
    })

})()

