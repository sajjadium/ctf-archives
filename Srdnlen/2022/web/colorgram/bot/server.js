const express = require('express') 
const app = express()
app.use(express.json());
const puppeteer = require('puppeteer')
const process = require('process')

const PORT = 8888
const URL_COLORGRAM = process.env['URL_COLORGRAM'] || "http://colorgram-app/";
const USERNAME = process.env['USERNAME'] || "admin";
const PASSWORD = process.env['PASSWORD'] || "REDACTED";
const TIMEOUT = 5000; // 5 seconds

async function open_url(color) {
    console.log('Running browser to visit "%s"', URL_COLORGRAM+'color.php?name='+USERNAME+'&color='+color);
	const browser = await puppeteer.launch({ 
        headless: true,
        args: [
            '--disable-setuid-sandbox',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--no-sandbox',
            '--safebrowsing-disable-auto-update'
        ]
    }, {executablePath: 'google-chrome-stable'})

	let page = await browser.newPage()
    await page.setDefaultNavigationTimeout(TIMEOUT);
	try{
        // Login
        console.log(URL_COLORGRAM+'login.php')
		await page.goto(URL_COLORGRAM+'login.php')
        await page.waitForSelector('#username')
        await page.focus('#username')
        await page.keyboard.type(USERNAME, {delay: 10})
        await page.waitForSelector('#username')
        await page.focus('#password')
        await page.keyboard.type(PASSWORD, {delay: 10})
        await Promise.all([
            page.click('button[type=submit]'),
            page.waitForNavigation({waitUntil: 'networkidle2'})
        ]);
		await page.goto(URL_COLORGRAM+'color.php?name='+USERNAME+'&color='+color)
        await new Promise(resolve => setTimeout(resolve, TIMEOUT));
		await page.close()
		await browser.close()
	} catch (e){
		await browser.close()
		console.log(e)
        //throw(e)
  	}

}
app.get('/request', async function (req, res) {
	res.set('Content-Type', 'text/html');
	const color = req.query.color;

	if (typeof color !== 'string'){
		console.log('Visit requested with missing parameters');
		res.status(400);
		res.send('Missing parameters');
		return;
	}
    try {
        open_url(color);
        res.send('ok');
        return;
    } catch (e) {
        console.log(e);
        res.status(500);
        res.send('failed');
        return;
    }
})

app.listen(PORT, '0.0.0.0');
console.log('Listening on port %d ...',PORT);