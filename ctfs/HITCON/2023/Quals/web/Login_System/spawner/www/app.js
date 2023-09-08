const express = require('express')
const session = require('express-session')
const crypto = require('crypto')
const cp = require('child_process')
const turnstile = require('./turnstile')

const TITLE = process.env.TITLE || 'Login System Spawner'
const IMAGE_NAME = process.env.IMAGE_NAME || 'login_system'
const TIMEOUT = parseInt(process.env.TIMEOUT || 60)
const TURNSTILE_SITE_KEY = process.env.TURNSTILE_SITE_KEY || '1x00000000000000000000AA'
const PORT_RANGE = (process.env.PORT_RANGE || '10000-11000').split('-').map(x => parseInt(x))

const app = express()
app.set('trust proxy', ['loopback', 'linklocal', 'uniquelocal'])
app.use(
	session({
		secret: crypto.randomBytes(20).toString('hex'),
		resave: true,
		saveUninitialized: false,
		name: 'spawner-sessid'
	})
)
app.use(express.urlencoded({ extended: false }))

app.get('/', (req, res) => {
	res.type('html').end(`
<!DOCTYPE html>
<head>
<title>${TITLE}</title>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
<style>body{font-family: Menlo, Consolas, Monaco, 'Liberation Mono', 'Lucida Console', monospace;}</style>
</head>
<body>
	<main>
	<h1>${TITLE}</h1>
	<article>
	The instance will be stopped after ${TIMEOUT} seconds, so please test the challenge locally first and create a new instance only when you are ready to solve it.
	${
		!req.session.info || +new Date() > +req.session.expiredAt
			? `<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
		<form method=post action=/create>
			<input type="text" name="captcha" style="display: none">
			<div class="cf-turnstile" data-sitekey="${TURNSTILE_SITE_KEY}"></div>
			<button type=submit>Create a new instance</button>
		</form>`
			: `<pre>${req.session.info}</pre>`
	}
	</article>
	</main>
</body>
	`)
})

const portsUsed = new Set()
app.post('/create', turnstile, (req, res) => {
	const username = crypto.randomBytes(8).toString('hex')
	const password = crypto.randomBytes(8).toString('hex')
	let port = 0
	while (portsUsed.has(port) || port === 0) {
		port = Math.floor(Math.random() * (PORT_RANGE[1] - PORT_RANGE[0] + 1)) + PORT_RANGE[0]
	}
	const instanceId = IMAGE_NAME + '-' + crypto.randomBytes(8).toString('hex')
	const command = `docker run --init --name ${instanceId} -d --rm -e TIMEOUT=${TIMEOUT} -p ${port}:${port} -e PORT=${port} -e HTTP_USERNAME=${username} -e HTTP_PASSWORD=${password} ${IMAGE_NAME}`
	console.log(`Running: ${command}`)
	cp.exec(command, err => {
		if (err)
			return res.send(
				`<b>Oops, something wrong: </b><pre>${err}</pre> (please report this error message to the challenge author)`
			)
		portsUsed.add(port)
		setTimeout(() => {
			portsUsed.delete(port)
		}, TIMEOUT * 1000)
		const url = `http://${req.hostname}:${port}/`
		const expiredAt = new Date(+new Date() + TIMEOUT * 1000)
		req.session.expiredAt = +expiredAt
		req.session.info = `Bot started!
Instance ID: ${instanceId}
Server: ${url}
HTTP Basic Auth Username: ${username}
HTTP Basic Auth Password: ${password}

This instance will be destroyed at ${expiredAt.toISOString()}.
`
		res.redirect('/')
	})
})

const port = process.env.PORT || 3001
app.listen(port, () => {
	console.log(`Listening on http://localhost:${port}`)
})
