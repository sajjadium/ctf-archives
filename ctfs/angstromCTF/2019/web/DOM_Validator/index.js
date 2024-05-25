var express = require('express')
var app = express()

app.use(express.urlencoded({ extended: false }))
app.use(express.static('public'))

app.get('/', function (req, res) {
	res.send(`<!doctype html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
</head>
<body style="background-color: black; text-align: center;">
<h1 style="color: white; margin-top: 2em;">Create Post</h1>
<form action='/posts' method='POST'>
<input name='title' placeholder='Post title'><br>
<textarea name='content' placeholder='Post content'></textarea><br>
<button type='submit' style="color: white">Create Post</button>
</form>
<h1 style="color: white">Report Post</h1>
<form action='/report' method='POST'>
<input name='url' placeholder='Post URL'><br>
<button type='submit' style="color: white">Report Post</button>
</form>
</body>
</html>`)
})

var fs = require('fs')
app.post('/posts', function (req, res) {
	// title must be a valid filename
	if (!(/^[\w\-. ]+$/.test(req.body.title)) || req.body.title.indexOf('..') !== -1) return res.sendStatus(400)
	if (fs.existsSync('public/posts/' + req.body.title + '.html')) return res.sendStatus(409)
	fs.writeFileSync('public/posts/' + req.body.title + '.html', `<!DOCTYPE html SYSTEM "3b16c602b53a3e4fc22f0d25cddb0fc4d1478e0233c83172c36d0a6cf46c171ed5811fbffc3cb9c3705b7258179ef11362760d105fb483937607dd46a6abcffc">
<html>
	<head>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
		<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/sha512.js"></script>
		<script src="../scripts/DOMValidator.js"></script>
	</head>
	<body>
		<h1>${req.body.title}</h1>
		<p>${req.body.content}</p>
	</body>
</html>`)
	res.redirect('/posts/' + req.body.title + '.html')
})

// admin visiting page
var puppeteer = require('puppeteer')
app.post('/report', async function (req, res) {
	res.sendStatus(200)
	try {
		var browser = await puppeteer.launch({
			args: ['--no-sandbox']
		})
		var page = await browser.newPage()
		await page.setCookie({
			name: 'flag',
			value: process.env.FLAG,
			domain: req.get('host')
		})
		await page.goto(req.body.url, {'waitUntil': 'networkidle0'})
	} catch (e) {
		console.log(e)
	}
})

app.listen(3002)
