const bodyParser = require('body-parser')
const cookieParser = require('cookie-parser');
const express = require('express')
const puppeteer = require('puppeteer')
const crypto = require('crypto')
const fs = require('fs')

const admin_id = "admin_"+crypto.randomBytes(32).toString('base64').split("+").join("_").split("/").join("$")
let flag = ""
fs.readFile('flag.txt', 'utf8', function(err, data) {  
    if (err) throw err;
    flag = data
});
const dom = "cookiemonster.2019.chall.actf.co"
let user_num = 0
const thecookie = {
	name: 'id',
	value: admin_id,
	domain: dom,
};

async function visit (url) {
	try{
		const browser = await puppeteer.launch({
			args: ['--no-sandbox']
		})
		var page = await browser.newPage()
		await page.setCookie(thecookie)
		await page.setCookie({name: "user_num", value: "0", domain: dom})
		await page.goto(url)
		await page.close()
		await browser.close()
	}catch(e){}
}

const app = express()

app.use(cookieParser())
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/style.css', express.static('style.css'));

app.use((req, res, next) => {
	var cookie = req.cookies?req.cookies.id:undefined
	if(cookie === undefined){
		cookie = "user_"+crypto.randomBytes(32).toString('base64').split("+").join("_").split("/").join("$")
		res.cookie('id',cookie,{maxAge: 1000 * 60 * 10, httpOnly: true, domain: dom})
		req.cookies.id=cookie
		user_num+=1
		res.cookie('user_num',user_num.toString(),{maxAge: 1000 * 60 * 10, httpOnly: true, domain: dom})
		req.cookies.user_num=user_num.toString();
	}
	if(cookie === admin_id){
		res.locals.flag = true;
	}else{
		res.locals.flag = false;
	}
	next()
})

app.post('/complain', (req, res) => {
	visit(req.body.url);
	res.send("<link rel='stylesheet' type='text/css' href='style.css'>okay")
})

app.get('/complain', (req, res) => {
	res.send("<link rel='stylesheet' type='text/css' href='style.css'><form method='post'><p>give me a url describing the problem and i will probably check it:</p><p><input name='url'></p><p><input type='submit'></p></form>")
})

app.get('/cookies', (req, res) => {
	res.end(Object.values(req.cookies).join(" "))
})

app.get('/getflag', (req, res) => {
	res.send("<link rel='stylesheet' type='text/css' href='style.css'>flag: "+(res.locals.flag?flag:"currently unavailable"))
})

app.get('/', (req, res) => {
	res.send("<link rel='stylesheet' type='text/css' href='style.css'>look this site is under construction if you have any complaints send them <a href='complain'>here</a>\n<!-- debug: /cookies /getflag -->")
})


app.use((err, req, res, next) => {
	res.status(500).send('error')
})

app.listen(3000)