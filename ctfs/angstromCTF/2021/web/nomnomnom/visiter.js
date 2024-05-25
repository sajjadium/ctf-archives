const puppeteer = require('puppeteer')
const fs = require('fs')

async function visit(secret, url) {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'], product: 'firefox' })
	var page = await browser.newPage()
	await page.setCookie({
		name: 'no_this_is_not_the_challenge_go_away',
		value: secret,
		domain: 'localhost',
		samesite: 'strict'
	})
	await page.goto(url)

	// idk, race conditions!!! :D
	await new Promise(resolve => setTimeout(resolve, 500));
	await page.close()
	await browser.close()
}

module.exports = { visit }
