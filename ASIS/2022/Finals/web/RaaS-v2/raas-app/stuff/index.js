#!/usr/bin/env node
const fastify = require('fastify')
const http = require('http')
const redis = require('redis')
const crypto = require('crypto')
const { Resolver } = require('node:dns')

const app = fastify()
const internalIps = ['127.0.0.1','0.0.0.0']
const client = redis.createClient({ url: 'redis://redis' })
const admins = {}

function convertIpToi64(ip){
	let [a,b,c,d] = ip.split('.')
	let ip64 = 0
	ip64 += (parseInt(a)<<24)+
			(parseInt(b)<<16)+
		    (parseInt(c)<<8) +
		    (parseInt(d))
	return ip64
}

function getPaymentAmount(){
	return crypto.randomInt(1e12)
}

function generateId(){
	return crypto.randomBytes(16).toString('hex')
}

function isIpOrHostnameSafe(host,dnsServer,callback,tries){
	if(typeof host != 'string'){
		callback(null)
		return false
	}

	let ip64 = convertIpToi64(host)
	if(ip64.toString() == 'NaN'){
		if(tries < 5) { fetchIp(host,dnsServer,callback,++tries) }
		else { callback(null) }
		return false
	}

	let ret = host 
	internalIps.forEach((ip)=>{
		if(convertIpToi64(ip) == ip64){
			ret = null
		}
	})
	callback(ret)
}

function addInternalAppIpToInternalIps(){
	return new Promise((resolve,reject)=>{
		const resolver = new Resolver()
		resolver.resolve('internal','A',(err, result)=>{
			if(err){ return reject()}
			internalIps.push(result[0])
			resolve()
		})
	})
}

async function getUser(userToken){
	let user = { isAdmin: false, username: null}
	if(userToken){
		let username = await client.get(`token:${userToken}`)
		if(username){
			user.isAdmin = admins[username] === true
			user.username = username
		}
	}
	return user
}

async function saveResponse(r){
	let id
	r = JSON.stringify(r)
	id = crypto.createHash('sha256').update(r).digest('hex')
	let result = await client.set(`resp:${id}`, r)
	if(result != 'OK'){ return false }
	return id
}

async function fetchIp(hostname,dnsServer,callback,tries=0){
	const resolver = new Resolver()
	resolver.setServers([dnsServer]) 
	resolver.resolve(hostname,'A',(err, result) => {
		let ip = err ? null : result[0]
		if(ip == null){
			resolver.resolve(hostname,'CNAME',(err, result) => {
				let hostname_ = err ? null : result[0]
				isIpOrHostnameSafe(hostname_,dnsServer,callback,tries)
			})
		} else {
			isIpOrHostnameSafe(ip,dnsServer,callback,tries)
		}
	})
}

async function fetch(p,callback){
	fetchIp(p.host,p.dnsServer,ip=>{
		if(ip == null){
			return callback(null)
		}
		try{
			let req = http.request(`http://${ip}:${p.port}/${p.path.slice(1)}`,{
				method: p.method,
				setHost: false,
				headers: p.headers,
			},(r)=>{
				let body = ''
				r.on('data',(data)=>{
					body += data.toString()
				})
				r.on('end',(data)=>{
					callback({ headers:r.headers, body: body.slice(0,1024*1024) })
				})
			})
			req.setTimeout(2000,_=>req.abort())

			req.on('error',_=>{ callback(null) })
			if(p.body){ req.write(p.body) }
			req.end()
		}catch(e){
			callback(null)
		}
	})
}

async function indexHandler(req,res){
	return {
		message: 'hi',
		success: true
	}
}

async function loginHandler(req,res){
	let userPassword, s, userToken
	const username = req.body?.username
	const password = req.body?.password

	s =  [
		typeof username == 'string',
		typeof password == 'string',
		/^\w{5,50}$/.test(username),
		/^\w{5,50}$/.test(password)
	]

	if(!s.every(e=>e)){
		return {
			success: false,
			message: 'Bad params'
		}
	}

	userToken = generateId()
	userPassword = await client.get(`user:${username}`)

	if(userPassword){
		if(userPassword != password){
			return {
				success: false,
				message: 'Wrong password',
			}
		}

		s = [
			await client.set(`token:${userToken}`,username) == 'OK',
			await client.expire(`token:${userToken}`, 60*10) == true
		]

		if(s.some(r=>r == false)){
			return {
				success: false,
				message: 'Could not save the token',
			}
		} 

		return {
			success: true,
			message: 'Logged in successfully',
			userToken
		}
	} else {
		s = [
			await client.set(`user:${username}`,password) == 'OK',
			await client.set(`token:${userToken}`,username) == 'OK',
			await client.expire(`token:${userToken}`, 60*10) == true
		]
		
		if(s.some(r=>r == false)){
			return {
				success: false,
				message: 'Could not register the user',
			}
		} 

		return {
			success: true,
			message: 'Logged in successfully',
			userToken
		}
	}
}

async function requestHandler(req,res){
	let user = await getUser(req.headers.token)
	const opts = {
		host: 'example.org',
		port: 80,
		path: '/',
		body: '',
		method: 'GET',
		dnsServer: '8.8.8.8',
		contentType: 'text/plain',
		...req.body
	}

	if( !/^[\w\.]+$/.test(opts.host) ||
		!Object.keys(opts).every(e=>
			['string','number'].includes(typeof opts[e]) && 
			!/internal/i.test(opts[e]) &&
			(e == 'body' && opts[e].toString().length < 1000) ||
			opts[e].toString().length < 100
		)
	){
		return {
			success: false,
			message: 'Bad params'
		}
	}

	opts.port = +opts.port
	opts.headers = {
		'Connection': 'close',
		'Host': `${opts.host}:${opts.port}`,
		'Content-Type': opts.contentType
	}

	if(opts.body.length){
		opts.headers['Content-Length'] = opts.body.toString().length
	} else {
		opts.body = null
	}

	return new Promise((resolve,_)=>{
		fetch(opts,async r=>{
			let paymentAmount

			if(r == null){ 
				return resolve({
					message: 'Request failed',
					success: false
				})
			}

			if(!user.isAdmin){
				paymentAmount = getPaymentAmount()
				r.body = `@@@@ pay $${paymentAmount} to admin to be able to see the response... or just be an admin maybe @@@@`
			}

			saveResponse(r).then(hash=>{
				let message = user.isAdmin ? 'Enjoy our services <3' : `You are not a premium user. Please pay $${paymentAmount} to enjoy the premium benefits.`
				if(hash == false) {
					return resolve({
						success: false,
						message: `Could not save the response`,
					})
				}
				resolve({
					success: true,
					message,
					id: hash,
				})
			})
		})
	})
}

async function responseHandler(req,res){
	let id = req.params.id
	let user = await getUser(req.headers.token)

	if(!user.isAdmin){
		let paymentAmount = getPaymentAmount()
		return {
			success: false,
			message: `You are not a premium user. Please pay $${paymentAmount} to enjoy the premium benefits.`
		}
	}
	return new Promise((resolve,_)=>{
		client.get(`resp:${id}`).then(resp=>{
			if(resp == null){ 
				resolve({
					success: false,
					message: 'Response not found'
				})
			} else {
				resolve({
					success: true,
					message: 'Response found',
					data: JSON.parse(resp)
				})
			}
		})
	})
}

async function errorHandler(err,req,res){
	res.status(500).send({ success: false, message: 'lol' })
}

(async ()=>{
	let aUsername = process.env.ADMIN_USERNAME || 'admin'
	let aPassword = process.env.ADMIN_PASSWORD || 'admin'

	app.get('/',indexHandler)
	app.post('/login',loginHandler)
	app.get('/response/:id',responseHandler)
	await app.register(require('@fastify/rate-limit'), {
	  max: 60,
	  timeWindow: '1 minute'
	})
	app.post('/request',requestHandler)
	app.setErrorHandler(errorHandler)
	await client.connect()
	if(await client.set(`user:${aUsername}`,aPassword) != 'OK'){
		console.log('[-] Could not register the admin')
		process.exit(1)
	}
	admins[aUsername] = true
	console.log(`[+] Admin's account: ${aUsername}:${aPassword}`)
	console.log('[+] connected to redis')

	await addInternalAppIpToInternalIps()
	app.listen({ port: 80, host: '0.0.0.0' },_=>console.log('[+] fastify is running on 80'))
})()