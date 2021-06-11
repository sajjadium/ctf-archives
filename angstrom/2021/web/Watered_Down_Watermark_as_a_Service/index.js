const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')
const puppeteer = require('puppeteer')
const express = require('express')
const crypto = require('crypto')
const sharp = require('sharp')
const bson = require('bson')
const zlib = require('zlib')
const fs = require('fs')

let flag = ""
fs.readFile('flag.txt', 'utf8', function(err, data) {  
    if (err) throw err;
    flag = data
});

const secretvalue = crypto.randomBytes(32).toString('hex')
const thecookie = {
	domain: "wdwaas.2021.chall.actf.co",
	name: "admin_cookie",
	value: secretvalue,
	httpOnly: true,
	secure: true,
	sameSite: 'None'
}

function checkURL(url) {
	const urlobj = new URL(url)
	if(!urlobj.protocol || !['http:','https:'].some(x=>urlobj.protocol.includes(x)) || urlobj.hostname.includes("actf.co")) return false
	return true
}

async function visit (url) {
	if (!checkURL(url)) throw URIError('no!!!')
	const browser = await puppeteer.launch({
		args: ['--no-sandbox', '--disable-setuid-sandbox']
	})
	let ctx = await browser.createIncognitoBrowserContext()
	let page = await ctx.newPage()
	page.on('framenavigated',function(frame){
		if (!checkURL(frame.url())) throw URIError('no!!!')
	})
	await page.setCookie(thecookie)
	await page.goto(url)
	const imageBuffer = await page.screenshot();
	const outputBuffer = await sharp(imageBuffer)
		.composite([{ input: "dicectf.png", gravity: "southwest" }]) // this was definitely not taken from dicectf trust me
		.toBuffer()
	await page.close()
	await ctx.close()
	return outputBuffer;
}

const app = express()

app.use(express.static('static'));
app.use(cookieParser());
app.use(bodyParser.urlencoded({extended:false}));

app.use((req, res, next) => {
	res.set('X-Frame-Options', 'deny');
	res.set('X-Content-Type-Options', 'nosniff');
	next()
})

app.get('/', (req, res) => {
	res.sendFile('static/index.html',{root:__dirname});
})

app.get('/add-flag', (req, res) => {
	let tmp_flag = flag
	if (req.cookies['admin_cookie'] !== secretvalue) {
		tmp_flag = "No flag for you!"
	}
	try {
		let object = {}
		if (req.query.object) {
			let tmp_obj = Buffer.from(req.query.object,'base64')
			if (parseInt(req.query.compressed)) {
				try { tmp_obj = zlib.inflateSync(tmp_obj);}
				catch(e){res.status(500).send("zlib error")}
			}
			object = bson.deserialize(tmp_obj)
		}
		object['flag'] = tmp_flag
		res.status(200).contentType('application/bson').send(bson.serialize(object));
	}catch (e) {res.status(500).send(e)}
})

app.get('/screenshot', async (req, res) => {
	const url = decodeURIComponent(req.query.url)
	try {
		const image = await visit(url);
		res.status(200).contentType('image/png').send(image);
	} catch (e) {
		if (e instanceof URIError) res.status(400).send('no!!!')
		else {
			console.log(e)
			res.sendStatus(500)
		}
	}
})


app.listen(3000,()=>console.log('yay'))