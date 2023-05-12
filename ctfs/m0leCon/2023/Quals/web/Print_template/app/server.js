const express = require('express')
const jwt = require('jsonwebtoken')
const fs = require('fs')
const cookieParser = require('cookie-parser')
const uuid = require('lil-uuid')
const fetch = require('node-fetch')
require('express-async-errors')

const FLAG = process.env.FLAG || 'ptm{test}'

const app = express()
const port = 3000

app.set('view engine', 'ejs');

const SECRET_KEY = process.env.SECRET_KEY || uuid()

const CHALL_URL = process.env.CHALL_URL || 'http://print.localtest.me:3000'
const SSO_URL = process.env.SSO_URL || 'http://sso.localtest.me:3001'
const SSO_URL_INT = process.env.SSO_URL_INT || 'http://sso:3001'
const CACHE_HOSTNAME = process.env.CACHE_HOSTNAME || 'localhost'

const SSO_URL_LOGIN = `${SSO_URL}/login?callback=${CHALL_URL}/cb`
const SSO_URL_REGISTER = `${SSO_URL}/register?callback=${CHALL_URL}/registered`
const SSO_CHECK_URL = `${SSO_URL_INT}/check-token`

const Memcached = require('memcached-promise');
const memcached = new Memcached(CACHE_HOSTNAME + ':11211');

const Tokens = require('csrf')
const csrf = new Tokens()

app.use(express.static('public'))
app.use(cookieParser())
app.use(express.urlencoded({extended: false}))  

app.use((req,res,next)=>{
    res.locals.errormsg = undefined
    res.locals.successmsg = undefined
    next()
})

async function get_template(user, id){
    return await memcached.get( 'template_' + user + '_' + id )
}

async function get_ntemplates(user){
    const n = await memcached.get( 'ntemplates_' + user )
    if (n === undefined){
        return 0
    }
    return parseInt(n)
}

async function set_template(user, id, value){
    await memcached.set( 'template_' + user + '_' + id, value, 0 )
    await memcached.set( 'ntemplates_' + user , id + 1, 0 )
}

async function get_printed(user, id_template, id_print){
    return await memcached.get( 'printed_' + user + '_' + id_template + '_' + id_print )
}

async function set_printed(user, id_template, id_print, value){
    await memcached.set( 'printed_' + user + '_' + id_template + '_' + id_print, value, 0 )
}

app.use((req, res, next)=> {
    res.locals.loggedUser = undefined
    res.locals.isPremium = false
    
    try {
        const decoded = jwt.verify(req.cookies.session, SECRET_KEY)
        //console.log(decoded)
        res.locals.loggedUser = decoded.user
        res.locals.isPremium = decoded.premium

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
    res.render('index')
})

app.get('/cb', async (req,res) => {
    try {
        if (req.query.token && typeof req.query.token === 'string'){
            const j = await (await fetch(SSO_CHECK_URL + '?token=' + encodeURIComponent(req.query.token))).json()
            if (j.user){
                const token = jwt.sign({ user: j.user, premium: j.premium }, SECRET_KEY);
                res.cookie('session', token)
                return res.redirect('/')
            }
        }
        return res.send('bad token')
    } catch {
        return res.send('Something is wrong, contact an admin')
    }
})

app.get('/', (req, res) => {

    const csrfsecret = csrf.secretSync()
    res.cookie('csrf', btoa(csrfsecret))

    return res.render('index', {flag: FLAG})

})

// only logged users in next endpoints and check csrf
app.use((req,res,next)=>{
    if (!res.locals.loggedUser){
        return res.status(403).send('Forbidden')
    }

    const csrfsecret = atob(req.cookies.csrf)
    res.locals.csrftoken = csrf.create(csrfsecret)

    if (req.method === 'POST'){
        if (!csrf.verify(csrfsecret, req.body.csrf) ){
            return res.send('Bad csrf')
        }
    }

    next()
})

app.get('/get-templates', (req,res)=>{
    template_names = fs.readdirSync(__dirname + '/public/templates')
    return res.render('get_templates', {template_names})
})

app.post('/get-templates', async (req,res)=>{
    let templates = req.body.templates
    if (!templates){
        return res.send('please, select a template')
    }

    if (!Array.isArray(templates)){
        if (typeof templates === 'string'){
            templates = [templates]
        } else {
            return res.status(400).send('bad request')
        }
    }

    //need to check the trial version limits
    if (templates.length > 1 && res.locals.isPremium !== true){
        res.locals.errormsg = 'Sorry, you can only import one template in the trial version'    
        return res.status(403).render('get_templates')
    }
    
    const regex_bad_filename = /\.\.|\//g

    for (let i=0; i<templates.length; i++){            
        const template = templates[i]
        if (regex_bad_filename.test(template) || !fs.existsSync(__dirname + '/public/templates/' + template)){
            res.locals.errormsg = 'Template not found'
        } else {
            const temp_text = fs.readFileSync(__dirname + '/public/templates/' + template, 'utf8')
            await set_template(res.locals.loggedUser, i, temp_text)
        }
    }
    if (!res.locals.errormsg){
        res.locals.successmsg = 'Imported successfully'
    }

    return res.render('get_templates')
})

app.post('/get-templates-url', async (req,res)=>{
    let {url} = req.body
    if (!url || typeof url !== 'string' || !url.startsWith('http')){
        return res.send('bad url')
    }

    const f_res = await fetch(url)
    if (f_res.status !== 200){
        res.locals.errormsg = 'Failed to fetch the template'
    } else {
        const temp_text = await f_res.text()
        await set_template(res.locals.loggedUser, 0, temp_text)
        res.locals.successmsg = 'Imported successfully'
    } 

    return res.render('get_templates')
})

app.get('/my-templates', async (req,res)=>{
    const n = await get_ntemplates(res.locals.loggedUser)
    let templates = []
    for (let i=0; i<n; i++){
        templates.push( (await get_template(res.locals.loggedUser,i) ))
    }
    return res.render('my_templates', {templates})
})


app.get('/my-templates/:id', async (req,res)=>{
    const regex_num = /^\d+$/g
    if (! regex_num.test(req.params.id)){
        return res.status(400).send('Invalid template id')
    }

    const template = (await get_template(res.locals.loggedUser,parseInt(req.params.id)) )

    if (!template){
        return res.status(404).send('Template not found')
    }
    
    return res.render('my_template', {template})
})

app.get('/print/:id', async (req,res)=>{
    const regex_num = /^\d+$/g
    if (! regex_num.test(req.params.id)){
        return res.status(400).send('Invalid template id')
    }

    const template = (await get_template(res.locals.loggedUser,parseInt(req.params.id)) )

    if (!template){
        return res.status(404).send('Template not found')
    }
    
    return res.render('print', {template})
})

app.post('/print/:id', async (req,res)=>{
    const regex_num = /^\d+$/g
    if (! regex_num.test(req.params.id)){
        return res.status(400).send('Invalid template id')
    }

    
    const tosub0 = req.body.tosub0
    const sub0 = req.body.sub0 ? (Array.isArray(req.body.sub0) ? req.body.sub0 : [req.body.sub0]) : []
    
    const tosub1 = req.body.tosub1
    const sub1 = req.body.sub1 ? (Array.isArray(req.body.sub1) ? req.body.sub1 : [req.body.sub1]) : []
    
    let template = (await get_template(res.locals.loggedUser,parseInt(req.params.id)) )

    if (!template){
        return res.status(404).send('Template not found')
    }

    let printid = 0
    for (let i=0; i<sub0.length; i++){

        const print_0 = template.split(tosub0).join(sub0[i])
        
        if(sub1.length > 0 && print_0.includes(tosub1)){
            for (let j=0; j<sub1.length; j++){
                const print_1 = print_0.split(tosub1).join(sub1[j])
                await set_printed(res.locals.loggedUser, req.params.id, printid, print_1)
                printid ++
            }
         } else {
            await set_printed(res.locals.loggedUser, req.params.id, printid, print_0)
            printid ++
        }
    }

    res.locals.successmsg = 'Printed!'
    return res.render('print', {template})
})

app.get('/view-print/:id', async (req,res)=>{
    const regex_num = /^\d+$/g
    if (! regex_num.test(req.params.id)){
        return res.status(400).send('Invalid template id')
    }
    
    return res.render('view_print',{templateid: req.params.id,  isPremium: res.locals.isPremium})
})

app.get('/printed/:idtemplate/:idprint', async (req,res)=>{
    
    const print = (await get_printed(res.locals.loggedUser,parseInt(req.params.idtemplate),parseInt(req.params.idprint)) )

    if (!print){
        return res.status(404).send('Print not found')
    }

    res.attachment('printedbyptm_' + req.params.idtemplate + '_' + req.params.idprint + '.txt');
    return res.send(print)
})

app.get('/view-print/:id', async (req,res)=>{
    const regex_num = /^\d+$/g
    if (! regex_num.test(req.params.id)){
        return res.status(400).send('Invalid template id')
    }

    const print = (await get_printed(res.locals.loggedUser,parseInt(req.params.idtemplate),parseInt(req.params.idprint)) )

    if (!print){
        return res.status(404).send('Print not found')
    }
    
    return res.render('printed_template',{print})
})
  
app.listen(port, () => {
    console.log(`App listening on port ${port}`)
})
