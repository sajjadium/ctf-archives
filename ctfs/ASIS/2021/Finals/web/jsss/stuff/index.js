#!/usr/bin/env node
const express = require('express')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const fs = require('fs')
const crypto = require('crypto')
const vm2 = require('vm2')
const child_process = require('child_process')

const app = express()
const hashPasswd = p=>crypto.createHash('sha256').update(p).digest('hex')
const rand = _ => crypto.randomBytes(Math.ceil(0x32/2)).toString('hex').slice(0,0x32);
const now = ()=>Math.floor(+new Date()/1000)
const users = new Set()
const flag = fs.readFileSync('/flag.txt').toString()
const secretMessage = process.env.SECRET_MESSAGE ?? ""
const checkoutTimes = new Map()
var lastUid = 0

app.use(cookieParser())
app.use(bodyParser.json())

app.use((req,res,next)=>{
	req.userUid = -1
	req.userOrder = ""

	let order = req.cookies.order
	let uid = req.cookies.uid
	let passwd = req.cookies.passwd

	if(uid == undefined || passwd == undefined)
		return next()

	let found = false
	for(let e of users.entries())
		if(e[0].uid == uid && e[0].password == passwd)
			found = true

	if(found){
		req.userUid = uid
		req.userOrder = order
	}

	next()
})

app.get('/',(req,res)=>{
	res.type('text/plain').send("hack me ( ﾟ▽ﾟ)/")
})

app.post('/login',(req,res)=>{
	let rUsername = req.body.username
	let rPassword = req.body.password

	if(!rUsername || !rPassword)
		return res.json({ error: true, msg: "Bad params" })

	let u = null
	for(let e of users.entries())
		if(e[0].username == rUsername)
			u = e[0]

	if(!u)
		return res.json({ error: true, msg: "User not found" })

	let hs = hashPasswd(rPassword.toString().slice(-0x20))
	if(u.password != hs)
		return res.json({ error: true, msg: "Wrong password" })

	res.cookie('uid',u.uid)
	res.cookie('passwd',hs)
	res.json({ error: false, msg: "Logged in" })
})

app.post('/register',(req,res)=>{
	let rUsername = req.body.username
	let rPassword = req.body.password

	if(!rUsername || !rPassword)
		return res.json({ error: true, msg: "Bad params" })

	for(let e of users.entries())
		if(e[0].username == rUsername)
			return res.json({ error: true, msg: "Username exists" })

	let hs = hashPasswd(rPassword.toString().slice(-0x20))
	let uid = lastUid++

	users.add({
		username: rUsername.toString().slice(-0x20),
		password: hs,
		uid: uid
	})

	res.cookie('uid',uid)
	res.cookie('passwd',hs)
	res.json({ error: false, msg: "Registered" })
})

app.post('/buy/:action',(req,res)=>{
	let ack = req.params.action
	let err = null
	if(ack == "sum"){
		if(!req.body.a || !req.body.b)
			err = "Bad params"
	} else err = "We don't support this action"

	if(err)
		return res.json({ error: true, msg: err})

	res.cookie('order',`${req.userOrder},${req.body.a},${req.body.b}`)
	res.json({ error: false, msg: "Order submitted" })
})

app.get('/checkout',(req,res)=>{
	if(req.userUid == -1 || !req.userOrder)
		return res.json({ error: true, msg: "Login first" })

	if(parseInt(req.userUid) != 0 || req.userOrder.includes("("))
		return res.json({ error: true, msg: "You can't do this sorry" })

	if(checkoutTimes.has(req.ip) && checkoutTimes.get(req.ip)+1 > now()){
		return res.json({ error: true, msg: 'too fast'})
	}
	checkoutTimes.set(req.ip,now())
	
	let sbx = {
		readFile: (path)=>{
			path = new String(path).toString()
			if(fs.statSync(path).size == 0)
				return null
			let r = fs.readFileSync(path)
			if(!path.includes('flag'))
				return r
			return null
		},
		sum: (args)=>args.reduce((a,b)=>a+b),
		getFlag: _=>{
			// return flag
			return secretMessage
		}
	}

	let vm = new vm2.VM({
		timeout: 20,
	    sandbox: sbx,
	    fixAsync: true,
	    eval: false
	})

	let result = ":("
	try{
		result = new String(vm.run(`sum([${req.userOrder}])`))
	}catch(e){}
	res.type('text/plain').send(result)
})

app.listen(8000,()=>console.log("Listening..."))
users.add({ username: "admin", password: hashPasswd(rand()), uid: lastUid++ })
