#!/usr/bin/env node
const express = require('express')
const session = require('express-session')
const crypto = require('crypto')
const puppeteer = require('puppeteer')

const app = express()
const users = new Map()
const notes = new Map()
const rand = _ => crypto.randomBytes(Math.ceil(0x20/2)).toString('hex').slice(0,0x20);
const flag = process.env.FLAG || 'ASIS{test-flag}'
const reportIpsList = new Map()
const now = ()=>Math.floor(+new Date()/1000)

app.use(session({
  secret: crypto.randomBytes(32).toString("base64"),
  resave: false,
  saveUninitialized: true,
  cookie: { sameSite: 'lax' }
}))
app.use(express.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.use((req,res,next)=>{
	res.setHeader('Content-Security-Policy',"script-src 'none' ;")
	res.setHeader('X-Content-Type-Options','nosniff')
	next()
})

app.get('/',(req,res)=>{
	if(!req.session.username)
		return res.redirect('/login')

	let q = req.query.search
	let userNotes = users.get(req.session.username).notes
	res.render('index',{ notes: userNotes })
})

app.post('/note',(req,res)=>{
	if(!req.session.username)
		return res.redirect('/login')

	let rTitle = req.body.title
	let rContent = req.body.content

	if(!rTitle || !rContent)
		return res.redirect('/')

	rTitle = rTitle.toString().slice(-0x30)
	rContent = rContent.toString().slice(-0x200)

	let noteId = rand()
	let u = users.get(req.session.username) 

	if(u.notes.length >= 10)
		return res.redirect('/')

	notes.set(noteId,rContent)
	u.notes.push({
		title: rTitle,
		id: noteId
	})

	return res.redirect('/')
})

app.get('/search',(req,res)=>{
	if(!req.session.username)
		return res.redirect('/login')

	let msg = (req.query.msg || 'Found note:\n').toString()
	let q  = (req.query.search || '').toString().slice(-0x40)

	res.type('text/plain')

	let userNotes = users.get(req.session.username).notes
	let foundNote = userNotes.find(e=>notes.get(e.id).includes(q))
	if(!foundNote)
		res.send('Not found')
	else
		res.send(msg+notes.get(foundNote.id))
})

app.get('/note/:noteid',(req,res)=>{
	if(!req.session.username)
		return res.redirect('/login')

	let u = users.get(req.session.username) 
	let note = notes.get(req.params.noteid)

	if(!note)
		return res.status(404).send("Not found")

	res.type('text/plain')
	res.send(note)
})

app.get('/report',(req,res)=>{
	let url = ""
	if(req.query.noteid)
		url = `http://${req.headers['host']}/note/${req.query.noteid}`
	res.render('report',{ url: url })
})

app.post('/report',async (req,res)=>{
	res.setHeader("Content-Type","text/plain")
	if(typeof req.body.url != "string" || !/^https?:\/\//.test(req.body.url)) return res.send("Bad url!")

	if(reportIpsList.has(req.ip) && reportIpsList.get(req.ip)+50 > now()){
		return res.send(`Please comeback ${reportIpsList.get(req.ip)+50-now()}s later!`)
	}
	reportIpsList.set(req.ip,now())

	const browser = await puppeteer.launch({ pipe: true,executablePath: '/usr/bin/google-chrome' })
	var page = await browser.newPage()

	await page.goto('http://localhost:8000/login')
	await page.waitForSelector("#usernameField");
	await page.type("#usernameField", rand());
	await page.type("#passwordField", rand());
	await page.click("#submitbtn")

	await page.waitForSelector("#titleField");
	await page.type("#titleField", "flag");
	await page.type("#contentField", flag);
	await page.click("#noteSubmitBtn")

	await page.close()

	page = await browser.newPage()
	res.send("Admin is visiting your url...")

	try{
		await page.goto(req.body.url,{
			timeout: 2000
		})
		await new Promise(resolve => setTimeout(resolve, 30e3));
	} catch(e){}
	await page.close()
	await browser.close()
})

app.post('/report',(req,res)=>{
	res.render('report')
})

app.get('/login',(req,res)=>{
	if(req.session.username)
		return res.redirect('/')
	res.render('login',{ error: null })
})

app.post('/login',(req,res)=>{
	let rUsername = req.body.username
	let rPassword = req.body.password

	if(req.session.username)
		return res.redirect('/')

	if(!rUsername || !rPassword)
		return res.render('login',{ error: "Bad params"})

	rUsername = rUsername.toString().trim().slice(-0x30)
	rPassword = rPassword.toString().trim().slice(-0x30)

	if(rUsername.length < 5 || rPassword.length < 5)
		return res.render('login',{ error: "Username and password should be longer than 5 characters"})

	let u = users.get(rUsername)
	if(u){
		if(u.password != rPassword)
			return res.render('login',{ error: "Wrong password"})
		req.session.username = rUsername
		return res.redirect('/')
	} else {
		users.set(rUsername,{
			password: rPassword,
			notes: []
		})
		req.session.username = rUsername
		return res.redirect('/')
	}
})

app.listen(8000,()=>console.log("Listening..."))
