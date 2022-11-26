const playwright = require('playwright-firefox')
const fs = require('fs')

const SITE = process.env.SITE || 'http://localhost:8763'
const CONTENT = fs.readFileSync(__dirname + '/secret.md', 'utf8')
const PREMIUM_TOKEN = process.env.PREMIUM_TOKEN || 'premium'

const visit = async url => {
	let browser
	try {
		browser = await playwright.firefox.launch({
			headless: true,
			firefoxUserPrefs: {
				'javascript.options.wasm': false,
				'javascript.options.baselinejit': false,
				// because crypto.subtle is only available in secure contexts
				'dom.securecontext.allowlist': new URL(SITE).hostname
			}
		})
		const ctx = await browser.newContext()
		await ctx.addCookies([
			{
				name: 'token',
				value: PREMIUM_TOKEN,
				url: SITE
			}
		])

		let page = await ctx.newPage()
		await page.goto(SITE, {
			waitUntil: 'networkidle'
		})
		await page.evaluate(content => {
			document.querySelector('input[name=title]').value = "admin's secret note"
			document.querySelector('textarea[name=content]').value = content
		}, CONTENT)
		await page.click('#markdown')
		await new Promise(resolve => setTimeout(resolve, 100))
		await page.click('#submit')
		await new Promise(resolve => setTimeout(resolve, 100))
		await page.waitForLoadState('networkidle')
		const resultUrl = await page.evaluate(() => document.querySelector('#result-url').value)
		console.log(`[+] Result URL: ${resultUrl}`)
		const urlNoKey = resultUrl.split('#')[0]
		console.log(`[+] URL without key: ${urlNoKey}`)
		await page.goto(resultUrl, {
			waitUntil: 'networkidle'
		})
		// Giving you the url of the secret should be safe because you don't have decryption key :)
		await page.goto(url + '?from=' + encodeURIComponent(urlNoKey))
		await page.waitForTimeout(30000)

		await browser.close()
		browser = null
	} catch (err) {
		console.log(err)
	} finally {
		if (browser) await browser.close()
	}
}

module.exports = visit

if (require.main === module) {
	visit('http://localhost:8001/')
}
