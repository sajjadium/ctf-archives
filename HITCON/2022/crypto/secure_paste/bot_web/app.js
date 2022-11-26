const express = require('express')
const net = require('net')
const hcaptcha = require('./hcaptcha')

const TITLE = process.env.TITLE || 'Admin Bot'
const PORT = process.env.PORT || 8000
const URL_CHECK_REGEX_RAW = process.env.URL_CHECK_REGEX || '^https?://.{1,256}$'
const URL_CHECK_REGEX = new RegExp(URL_CHECK_REGEX_RAW)
const HCAPTCHA_SITE_KEY = process.env.HCAPTCHA_SITE_KEY || '10000000-ffff-ffff-ffff-000000000001'
const BOT_HOST = process.env.BOT_HOST || 'localhost'
const BOT_PORT = process.env.BOT_PORT || 7777

const INDEX_HTML = `
<!DOCTYPE html>
<head>
<title>${TITLE}</title>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
</head>
<body>
<main>
<h1>${TITLE}</h1>
<form action="/submit" method="POST" class="form">
    <input type="text" name="captcha" style="display: none">
    <p>
        <label>URL</label>
        <input type="text" name="url" pattern="${URL_CHECK_REGEX_RAW}" required>
    </p>
    <p>
        <div class="h-captcha" data-sitekey="${HCAPTCHA_SITE_KEY}"></div>
    </p>
    <p>
        <button type="submit">Submit</button>
    </p>
</form>
<script src="https://js.hcaptcha.com/1/api.js" async defer></script>
</main>
</body>
`

const app = express()
app.use(express.urlencoded({ extended: false }))

app.get('/', (req, res) => {
	res.send(INDEX_HTML)
})
app.post('/submit', hcaptcha, (req, res) => {
	const { url } = req.body
	if (!url || !URL_CHECK_REGEX.test(url)) {
		return res.status(400).send('Invalid URL')
	}
	console.log(`[+] Sending ${url} to bot`)

	try {
		const client = net.connect(BOT_PORT, BOT_HOST, () => {
			client.write(url)
		})

		let response = ''
		client.on('data', data => {
			response += data.toString()
			client.end()
		})

		client.on('end', () => res.send(response))
	} catch (e) {
		console.log(e)
		res.status(500).send('Something is wrong...')
	}
})

app.listen(PORT, () => {
	console.log(`Listening on http://localhost:${PORT}`)
})
