const express = require('express')
const { spawn } = require('node:child_process');

const TITLE = process.env.TITLE || 'Admin Bot'
const PORT = process.env.PORT || 8000
const URL_CHECK_REGEX_RAW = process.env.URL_CHECK_REGEX || '^https?://.{1,256}$'
const URL_CHECK_REGEX = new RegExp(URL_CHECK_REGEX_RAW)

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
        <button type="submit">Submit</button>
    </p>
</form>
</main>
</body>
`

const app = express()
app.use(express.urlencoded({ extended: false }))

app.get('/', (req, res) => {
	res.send(INDEX_HTML)
})
app.post('/submit', async (req, res) => {
	const { url } = req.body
	if (!url || !URL_CHECK_REGEX.test(url)) {
		return res.status(400).send('Invalid URL')
	}

	try {
		console.log(`[+] Sending ${url} to bot`)
		spawn('node', ['bot.js', url], { stdio: 'inherit' })
		res.send('OK')
	} catch (e) {
		console.log(e)
		res.status(500).send('Something is wrong...')
	}
})

app.listen(PORT, () => {
	console.log(`Listening on http://localhost:${PORT}`)
})
