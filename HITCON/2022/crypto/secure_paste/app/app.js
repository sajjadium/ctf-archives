const express = require('express')
const cookieParser = require('cookie-parser')
const crypto = require('crypto')
const utils = require('./utils')
const fs = require('fs')

const PREMIUM_TOKEN = process.env.PREMIUM_TOKEN || 'premium'

const bundlejs = (() => {
	// poor man's javascript bundler
	const DIR = 'static/js'
	let js = ''
	for (const f of ['utils.js', 'crypto.js', 'fputils.js', 'jsonplus.js']) {
		js += fs.readFileSync(`${DIR}/${f}`, 'utf-8') + '\n'
	}
	return js
})()

const db = new utils.Database()
const app = express()

app.set('view engine', 'ejs')
app.use((req, res, next) => {
	const nonce = crypto.randomBytes(16).toString('hex')
	res.locals.nonce = nonce
	res.set(
		'Content-Security-Policy',
		`default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline'; img-src *; frame-src 'none'; object-src 'none'`
	)
	res.set('X-Frame-Options', 'DENY')
	res.set('X-Content-Type-Options', 'nosniff')
	next()
})
app.use('/static', express.static('static'))
app.get('/static/js/bundle.js', (req, res) => res.set('Content-Type', 'text/javascript').end(bundlejs))
app.use(express.json({ limit: '10kb' }))
app.use(cookieParser())

app.get('/', (req, res) => {
	return res.render('index')
})
app.get('/paste', (req, res) => {
	return res.render('paste')
})
app.post('/api/pastes', (req, res) => {
	const isPremium = req.cookies.token === PREMIUM_TOKEN
	const payload = req.body
	if (!utils.setEqual(new Set(['content', 'type']), new Set(Object.keys(payload)))) {
		return res.status(403).json({
			error: 'Invalid payload'
		})
	}
	if (payload.type !== 'plain' && !isPremium) {
		return res.status(403).json({
			error: `Sorry, but ${payload.type} is only available for premium users. You can upgrade to premium by sending the author 21 million Bitcoin.`
		})
	}
	const id = db.put(payload)
	return res.json({
		success: true,
		id
	})
})
app.get('/api/pastes/:id', (req, res) => {
	const data = db.get(req.params.id)
	res.jsonp(
		data || {
			error: 'Paste not found'
		}
	)
})

const port = process.env.PORT || 8763
app.listen(port, () => {
	console.log(`Server listening on port http://localhost:${port}`)
})

// For local testing convenience:
// ;(async () => {
// 	const CryptoUtils = require('./static/js/crypto')
// 	const jsonplus = require('./static/js/jsonplus')
// 	const cu = new CryptoUtils()
// 	const key = await cu.genkey('raw')
// 	const secret = fs.readFileSync('../bot/secret.md', 'utf-8')
// 	const pt = JSON.stringify({
// 		title: "admin's secret note",
// 		content: secret
// 	})
// 	const result = await cu.encrypt({ key, pt })
// 	const deckey = btoa(jsonplus.serialize({ key, iv: result.iv }))
// 	const id = db.put(
// 		JSON.parse(
// 			jsonplus.serialize({
// 				type: 'markdown',
// 				content: result.ct
// 			})
// 		)
// 	)
// 	console.log(`http://localhost:${port}/paste?id=${id}#${deckey}`)
// })()
