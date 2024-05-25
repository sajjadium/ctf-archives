const jason = require('./jason')

const express = require('express')
const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser')

const app = express()

function sameOrigin (req, res, next) {
	if (req.get('referer') && !req.get('referer').startsWith(process.env.URL))
		return res.sendStatus(403)
	return next()
}

app.use(bodyParser.urlencoded({ extended: false }))
app.use(cookieParser())

app.use(express.static('public'))

app.post('/passcode', function (req, res) {
	if (req.body.passcode === 'CLEAR') res.append('Set-Cookie', 'passcode=')
	else res.append('Set-Cookie', `passcode=${(req.cookies.passcode || '')+req.body.passcode}`)
	return res.redirect('/')
})

app.post('/visit', async function (req, res) {
	if (req.body.site.startsWith('http')) try {await jason.visit(req.body.site) } catch (e) {console.log(e)}
	return res.redirect('/')
})

app.get('/languages', sameOrigin, function (req, res) {
	res.jsonp({category: 'languages', items: ['C++', 'Rust', 'OCaml', 'Lisp', 'Physical touch']})
})

app.get('/friends', sameOrigin, function (req, res) {
	res.jsonp({category: 'friends', items: ['Functional programming']})
})

app.get('/flags', sameOrigin, function (req, res) {
	if (req.cookies.passcode !== process.env.PASSCODE) return res.sendStatus(403)
	res.jsonp({category: 'flags', items: [process.env.FLAG]})
})

app.listen(7331)
