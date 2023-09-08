const express = require('express')
const session = require('express-session')
const crypto = require('crypto')
const cp = require('child_process')
const turnstile = require('./turnstile')

const TITLE = process.env.TITLE || 'Harmony Bot Spawner'
const IMAGE_NAME = process.env.IMAGE_NAME || 'harmony_bot'
const TIMEOUT = parseInt(process.env.TIMEOUT || 60)
const APP_SERVER = process.env.APP_SERVER || 'http://localhost:3000'
const TURNSTILE_SITE_KEY = process.env.TURNSTILE_SITE_KEY || '1x00000000000000000000AA'

const app = express()
app.use(
	session({
		secret: crypto.randomBytes(20).toString('hex'),
		resave: true,
		saveUninitialized: false
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
app.post('/create', turnstile, (req, res) => {
	const channel = crypto.randomBytes(8).toString('hex')
	const instanceId = IMAGE_NAME + '-' + crypto.randomBytes(8).toString('hex')
	// --network=host is only needed if your are testing the challenge locally, or you can do it properly by configuring `server` container to a publicly accessible address
	// const command = `docker run --network=host --init --name ${instanceId} -d --rm -e TIMEOUT=${TIMEOUT} -e SERVER=${APP_SERVER} -e CHANNEL=${channel} ${IMAGE_NAME}`
	const command = `docker run --init --name ${instanceId} -d --rm -e TIMEOUT=${TIMEOUT} -e SERVER=${APP_SERVER} -e CHANNEL=${channel} ${IMAGE_NAME}`
	console.log(command)
	cp.exec(command, err => {
		if (err)
			return res.send(
				`<b>Oops, something wrong: </b><pre>${err}</pre> (please report this error message to the challenge author)`
			)
		const expiredAt = new Date(+new Date() + TIMEOUT * 1000)
		req.session.expiredAt = +expiredAt
		req.session.info = `Bot started!
Instance ID: ${instanceId}
Server: ${APP_SERVER}
Channel: ${channel}

This instance will be destroyed at ${expiredAt.toISOString()}.
`
		res.redirect('/')
	})
})

const port = process.env.PORT || 3001
app.listen(port, () => {
	console.log(`Listening on http://localhost:${port}`)
})
