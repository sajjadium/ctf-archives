const puppeteer = require('puppeteer')
const fs = require('fs')

async function register(password) {
	try
	{
	const browser = await puppeteer.launch({ args: ['--no-sandbox'], headless: false})
	var page = await browser.newPage()
    await page.goto('http://localhost:8080/register')
	await page.type("#username", 'admin')
    await page.type("#password",password)
	await page.focus("#flag");
	await page.keyboard.down('Control');
	await page.keyboard.press('A');
	await page.keyboard.up('Control');
	await page.keyboard.press('Backspace');
	await page.type("#flag", `${process.env.FLAG}`)
	await Promise.all([
		page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10002 }),
		page.click('#submit'),
	  ])
	await page.close()
	await browser.close()
	}catch (e) {
		console.log("Error", e)
	  }
}


async function visit(url, password) {
	try{
	const browser = await puppeteer.launch({ args: ['--no-sandbox'], headless: false})
	var page = await browser.newPage()
    await page.goto('http://localhost:8080/login')
	await page.type("#username", 'admin')
    await page.type("#password",password)
    await Promise.all([
		page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10002 }),
		page.click('#submit'),
	  ])
	await Promise.all([
		page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10002 }),
		await page.goto(url)
	  ])
	await page.close()
	await browser.close()
	}
	catch (e) {
		console.log("Error", e)
	  }
}

module.exports = { visit, register}
