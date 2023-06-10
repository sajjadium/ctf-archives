const puppeteer = require('puppeteer')

const domain = process.env["INTERNAL_DOMAIN"] || "flagify3_frontend";

const username = "admin"
const password = process.env["ADMIN_PASSWORD"] || "password"

async function visit(url) {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] })

	var page = await browser.newPage()

	try {
		console.error("Doing login")
		await page.goto(`http://${domain}/login`);
		await new Promise(resolve => setTimeout(resolve, 1000));

		await page.type('#username', username);
		await page.type('#password', password);
		await page.click('#submit');
		console.error("Submitted login form")

		await new Promise(resolve => setTimeout(resolve, 2000));

		// visit reported page
		await page.goto(url)
		await new Promise(resolve => setTimeout(resolve, 5000));
		console.error('Ending wait')

		await page.close()
		await browser.close()
	} catch (e) {
		await browser.close()
		throw (e)
	}

}

module.exports = { visit }
