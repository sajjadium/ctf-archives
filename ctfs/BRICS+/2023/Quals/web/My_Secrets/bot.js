const puppeteer = require('puppeteer')
const sleep = async ms => new Promise(resolve => setTimeout(resolve, ms))

let browser = null

const visit = async url => {
	let context = null
	try {
		if (!browser) {
			const args = ['--js-flags=--jitless,--no-expose-wasm', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox']
			if (new URL(url).protocol === 'http:') {
				args.push(`--unsafely-treat-insecure-origin-as-secure=${url}`)
			}
			browser = await puppeteer.launch({
				headless: 'new',
				args
			})
		}
		
		context = await browser.createIncognitoBrowserContext()
		const page1 = await context.newPage()
		await page1.goto("https://mysecrets-8a88458a82b93f84.brics-ctf.ru/users/login")

		await page1.type('input[name=username]', 'slonser');
		await page1.type('input[name=password]', 'Are you crazyman?');
	  
		// Submit the form
		await page1.click('button[type=submit]');
	  
		// Wait for a navigation event to ensure the form submission has completed
		await sleep(2000)
	  	console.log("Abobus")
		await page1.goto(url)
		await sleep(10000)
		await page1.close()
		await context.close()
		context = null
	} catch (e) {
		console.log(e)
	} finally {
		if (context) await context.close()
	}
}
module.exports = visit;
