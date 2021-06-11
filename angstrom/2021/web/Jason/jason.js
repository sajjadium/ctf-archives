const puppeteer = require('puppeteer')
const fs = require('fs')

async function visit(url) {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
	var page = await browser.newPage()
	await page.goto(process.env.URL)
	await page.waitForSelector('input[value="CLEAR"]')
	for (let i = 0; i < process.env.PASSCODE.length; i++) {
		await Promise.all([
			page.waitForNavigation(),
			page.click(`input[value="${process.env.PASSCODE[i]}"]`)
		])
	}
	await page.goto(url, { waitUntil: 'networkidle2' })
	await page.close()
	await browser.close()
}

module.exports = { visit }
