
const express = require('express')
const jwt = require('jsonwebtoken')
const crypto = require('crypto')
const cookieParser = require('cookie-parser')
const bcrypt = require('bcrypt')
require('express-async-errors')

const knex = require('knex')({
    client: 'better-sqlite3',
    connection: {
      filename: ":memory:",
    },
    useNullAsDefault: true,
  });
  

const CHALL_URL = process.env.CHALL_URL || 'http://app.localtest.me:3000'
const SSO_URL = process.env.SSO_URL || 'http://sso.localtest.me:3001'
const REPORT_URL = process.env.REPORT_URL || 'http://headless:5000/'
const AUTH_TOKEN_REPORT = process.env.AUTH_TOKEN_REPORT || 'supersecret'

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || crypto.randomUUID()

const SECRET_KEY = process.env.SECRET_KEY || crypto.randomUUID()

const app = express()
const port = 3001

app.set('view engine', 'ejs');

app.use(cookieParser())
app.use(express.urlencoded({extended: false}))

app.use((req,res,next)=>{
    res.locals.errormsg = undefined
    res.locals.successmsg = undefined
    next()
})

function check_callback(host){
    console.log(host)
    return host.startsWith(`${CHALL_URL}/cb`);
}

async function new_token(user){
    const t = crypto.randomBytes(20).toString('base64url')
    await knex('tokens').insert({username: user, token: t})
    return t
}
 
app.get('/login', async (req, res)=>{

    try {
        const decoded = jwt.verify(req.cookies.sessionsso, SECRET_KEY)
        if (req.query.callback && check_callback(req.query.callback)){
            return res.redirect(req.query.callback + '#' + (await new_token(decoded.user)))
        }
    } catch {
    }
    res.render('login')

})

app.get('/register', (req, res)=>{
    res.render('register')
})

app.post('/login', async (req, res) => {

    if (!req.body.username || typeof req.body.username !== 'string'){
        return res.status(400).send('')
    }

    const r = await knex.select('password').from('users').where('username','=',req.body.username).first()

    if (!r){
        res.locals.errormsg = 'Bad credentials'
        return res.render('login')
    }
    if (!bcrypt.compareSync(req.body.password, r.password)){
        res.locals.errormsg = 'Bad credentials'
        return res.render('login')
    } 
    
    const token = jwt.sign({ user: req.body.username }, SECRET_KEY);
    res.cookie('sessionsso', token)

    if (req.query.callback && check_callback(req.query.callback)){
        return res.redirect(req.query.callback + '#' + (await new_token(req.body.username)))
    }

    return res.redirect('/')
})

app.post('/register', async (req, res) => {

    if (!req.body.username || typeof req.body.username !== 'string'){
        return res.status(400).send('')
    }

    try {
        await knex('users').insert({username: req.body.username, password: bcrypt.hashSync(req.body.password,10)})
    } catch (e){
        res.locals.errormsg = 'User already exists'
        return res.render('register') 
    }

    if (req.query.callback){
        return res.redirect(req.query.callback)
    } else {
        res.locals.successmsg = 'Registered!'
        return res.render('register') 
    }
})

app.get('/check-token', async (req,res)=>{
    const r = await knex.select('username').from('tokens').where('token','=',req.query.token).first()

    if (!r){
        return res.json({user: null})
    }
    
    // delete the token
    await knex('tokens').where('token','=',req.query.token).del()
    
    return res.json({user: r.username})
})


app.get('/', (req, res) => {

    let loggedUser = undefined
    try {
        const decoded = jwt.verify(req.cookies.sessionsso, SECRET_KEY)
        loggedUser = decoded.user
    } catch {
    }

    res.render('home', {loggedUser})
});



app.get('/report', async (req, res)=>{

    let loggedUser = undefined

    try {
        const decoded = jwt.verify(req.cookies.sessionsso, SECRET_KEY)
        loggedUser = decoded.user
    } catch {
    }
    
    if (!loggedUser){
        return res.redirect('/login')
    }

    return res.render('report')
});


async function visit_url(url){
    console.log(url)
    if (!url || typeof url !== 'string'){
        throw Error('Bad URL')
    }

    if (url.startsWith('http://') || url.startsWith('https://')){

        const admin_cookie = jwt.sign({ user: 'admin' }, SECRET_KEY);
        const actions = [
            {type: 'request', url: SSO_URL},
            {type: 'set-cookie', name: 'sessionsso', value: admin_cookie},
            {type: 'request', url: url},
            {type: 'sleep', time: 5},
        ]

        const r = await fetch(REPORT_URL, {
            method: 'POST',
            body: JSON.stringify({actions, browser: 'firefox'}),
            headers: {
                'Content-Type': 'application/json',
                'X-Auth': AUTH_TOKEN_REPORT
            }
        })

        if (r.status !== 200){
            console.error(r.status)
            console.error((await r.text()))
            throw Error('Headless is not working')
        }

        return true
    } else {
        throw Error('Bad URL')   
    }
    
}

app.post('/report', async (req, res)=>{
    let loggedUser = undefined

    try {
        const decoded = jwt.verify(req.cookies.sessionsso, SECRET_KEY)
        loggedUser = decoded.user
    } catch {
    }
    
    if (!loggedUser){
        return res.redirect('/login')
    }

    try {
        await visit_url(req.body.url)
        res.locals.successmsg = 'An admin will visit your url soon'
    } catch (e) {
        res.locals.errormsg = e.toString()
    }

    return res.render('header')
});


(async () => {

    // create empty db
    await knex.schema.dropTableIfExists('users')
    await knex.schema.dropTableIfExists('token')

    await knex.schema.createTable('users', function (table) {
        table.string('username',40).primary()
        table.string('password')
    })

    await knex.schema.createTable('tokens', function (table) {
        table.string('username',40)
        table.string('token',40)
    })


    await knex('users').insert({username: 'admin', password: bcrypt.hashSync(ADMIN_PASSWORD,10)})

    console.log('Admin password: ' + ADMIN_PASSWORD)

    // start the server
    app.listen(port, () => {
    console.log(`App listening on port ${port}`)
    })
    
})()