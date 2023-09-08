const puppeteer = require('puppeteer')

const SITE = process.env.SITE || 'http://localhost:8763'
const FLAG = process.env.FLAG || 'test{flag}'
const CODE = `f=${JSON.stringify(FLAG)};l=f.length
c.width=1920
x.font="200px Arial"
for(i=0;i<l;i++){x.fillStyle=R(128+S(T(t)-i)*70,128+C(T(t)+i)*70,128+S(T(t)-l-i)*70,1.0);x.fillText(f[i],300+i*60+C(T((t-i/l)/1.8)-i)*400,540+S(T((t-i/l)/1.5)-i)*800)}`

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
		await page1.goto(SITE + '/?code=' + encodeURIComponent(CODE))
		await sleep(1000)
		await page1.close()

		const page2 = await context.newPage()
		page2.goto(url)
		await sleep(5000)
		await page2.close()

		await context.close()
		context = null
	} catch (e) {
		console.log(e)
	} finally {
		if (context) await context.close()
	}
}

module.exports = visit

if (require.main === module) {
	visit('http://example.com')
}
