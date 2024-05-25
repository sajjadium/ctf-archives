var express = require('express')
var cookieParser = require('cookie-parser')
var bodyParser = require('body-parser')
var app = express()
app.use(cookieParser())
app.use(bodyParser.urlencoded({ extended: false }))

var crypto = require('crypto')
var querystring = require('querystring')
var url = require('url')
var bent = require('bent')

var { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
	modulusLength: 2048,    
		publicKeyEncoding: {
		type: 'spki',
		format: 'pem'
	},   
	privateKeyEncoding: {
		type: 'pkcs8',
		format: 'pem'
	} 
})
var flags = [
	{name: 'picoCTF', flag: 'picoCTF{who_stole_our_flags}'},
	{name: 'RedpwnCTF', flag: 'guessCTF{cOoKiE_ReCiPiEs}'},
	{name: 'HSCTF', flag: 'hsctf{hacked_by_REDPWN}'},
	{name: 'ångstromCTF', flag: process.env.FLAG, hidden: true}
]
var src = "#include \"stdio.h\"\nint main() { puts(\"FLAG\"); }"
var headers = {'content-type': 'application/octet-stream', 'content-disposition': 'attachment'}
var headersToSign = Object.keys(headers).sort().map(h => h+': '+headers[h]).join('\n')
var keyId = crypto.createHash('sha256').update(privateKey).digest('hex')
async function buildFlags() {
	for (var i = 0; i < flags.length; i++) {
		var res = await bent('POST', 'json')(process.env.UBI+'/build', Buffer.from(`referer=${process.env.URL}/&src=${encodeURIComponent(src.replace("FLAG", flags[i].flag))}&key=${encodeURIComponent(privateKey)}`), {'content-type': 'application/x-www-form-urlencoded'})
		var sig = crypto.publicEncrypt(publicKey, crypto.createHash('sha256').update(headersToSign+`\nx-ubi-id: ${res.id}\nx-ubi-key: ${keyId}`).digest()).toString('hex')
		flags[i].url = process.env.URL+'/download/'+res.id+'/flag?'+querystring.stringify(headers)+'&sig='+sig
	}
}
buildFlags()

app.use(function (req, res, next) {
	res.set({'content-security-policy': 'script-src \'none\';'})
	next()
})

app.get('/', function (req, res) {
	res.send(`<!DOCTYPE html>
<html>
	<head>
		<title>Flags</title>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="/style.css">
	</head>
	<body>
		<section class="section">
			<div class="container">
				<div class="tile is-ancestor is-vertical">
					<div class="tile is-parent"><div class="tile is-child">
						<h1 class="title is-1">Flags</h1>
						<form method="POST" action="/submit">
							<div class="field"><p>Are we missing a flag you think we should have? Send us a link and an admin will check it out!</p></div>
							<div class="field"><div class="control">
								<input class="input" type="text" name="url" placeholder="Flag URL">
							</div></div>
							<div class="field"><div class="control">
								<button class="button" type="submit">Submit</button>
							</div></div>
						</form>
					</div></div>
					${flags.map(flag => (!flag.hidden || req.cookies.admin === process.env.ADMIN) ? `<div class="tile is-parent"><div class="tile is-child box">
						<p class="title">${flag.name}</p>
						<p><a href="${flag.url}" class="button">Download Flag</a></p>
					</div></div>` : '').join('')}
				</div>
			</div>
		</section>
	</body>
</html>`)
})

app.get('/style.css', function (req, res) {
	res.sendFile(__dirname+'/style.css')
})

app.get('/download/:file(*)', function (req, res) {
	var proxyHeaders = req.headers
	delete proxyHeaders.host
	bent(process.env.UBI, 200, 400, proxyHeaders)('/'+req.params.file+'?'+url.parse(req.url).query).then(function (response) {
		if (response.headers['x-ubi-key'] !== keyId) return res.status(404).end()
		res.status(response.statusCode)
		for (var h in response.headers) {
			if (!res.get(h)) res.set(h, response.headers[h])
		}
		response.on('data', function (chunk) {
			res.write(chunk)
		})
		response.on('close', function () {
			res.end()
		})
		response.on('end', function () {
			res.send()
		})
	}).catch(async function (error) {
		res.status(404).end()
	})
})

/* admin visitor */
var puppeteer = require('puppeteer')
app.post('/submit', async function (req, res) {
	try {
		if (!(req.body.url && (req.body.url.startsWith('http://') || req.body.url.startsWith('https://')))) return res.status(400).end()
		var browser = await puppeteer.launch({
			args: ['--no-sandbox']
		})
		var page = await browser.newPage()
		await page.setCookie({
			name: 'admin',
			value: process.env.ADMIN,
			url: process.env.URL,
			httpOnly: true
		})
		await page.goto(req.body.url, { waitUntil: 'networkidle0' })
		await new Promise(r => setTimeout(r, 10000));
		await page.close()
		await browser.close()
		res.redirect('/')
	} catch (e) {
		res.status(500).end()
	}
})

app.listen(5001)
