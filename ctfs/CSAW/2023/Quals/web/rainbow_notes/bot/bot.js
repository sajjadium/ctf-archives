const puppeteer = require('puppeteer')

const SITE = process.env.SITE || 'http://web'
const FLAG = process.env.FLAG || 'csawctf{test_flag}'
const NOTE = `I heard you like flags, here you go: ${FLAG}`

const sleep = async ms => new Promise(resolve => setTimeout(resolve, ms))

let browser = null

const visit = async url => {
	let context = null
	try {
		if (!browser) {
			const args = ['--js-flags=--jitless,--no-expose-wasm', '--disable-gpu', '--disable-dev-shm-usage']
			if (new URL(SITE).protocol === 'http:') {
				// for testing locally
				// we need this for Sanitizer API as `http://web` is considered insecure
				args.push(`--unsafely-treat-insecure-origin-as-secure=${SITE}`)
			}
			browser = await puppeteer.launch({
				headless: 'new',
				args
			})
		}

		context = await browser.createIncognitoBrowserContext()

		const page1 = await context.newPage()
		await page1.goto(SITE + '/?note=' + encodeURIComponent(NOTE))
		await sleep(1000)
		await page1.close()

		const page2 = await context.newPage()
		console.log(`[+] Visiting ${url}`)
		page2.goto(url)
		await sleep(2000)
		await page2.close()

		await context.close()
		console.log('[+] Done')
		context = null
	} catch (e) {
		console.log(e)
	} finally {
		if (context) await context.close()
	}
}

module.exports = visit

if (require.main === module) {
	visit(process.argv[2])
}
