const crypto = require('crypto');
const puppeteer = require('puppeteer');
let queue = [];

async function run(username,password) {
	let browser;

	try {
		module.exports.open = true;
		browser = await puppeteer.launch({
			headless: true,
			pipe: true,
			args: ['--incognito', '--no-sandbox', '--disable-setuid-sandbox'],
			slowMo: 10
		});

		let page = (await browser.pages())[0];

		await page.goto('http://localhost:8080/register');
		await page.type('[name="username"]', crypto.randomBytes(8).toString('hex'));
		await page.type('[name="nickname"]', "CodeTiger");
		await page.type('[name="decade"]', "OMG I LOVE THE <b>2000s</b> It's just like so <i>HYPE</i>");
		await page.type('[name="password"]', crypto.randomBytes(8).toString('hex'));


		await Promise.all([
			page.click('[type="submit"]'),
			page.waitForNavigation({ waituntil: 'domcontentloaded' })
		]);

		await page.goto('http://localhost:8080/new');
		await page.type('[name="url"]', 'https://hospitalnews.com/wp-content/uploads/2013/07/red-flag.png');
		await page.type('[name="description"]', "OMG LOOK AT MY NEW FLAG -> " + (process.env.FLAG ?? 'ctf{flag}'));

		await Promise.all([
			page.click('[type="submit"]'),
			page.waitForNavigation({ waituntil: 'domcontentloaded' })
		]);

		await page.goto('http://localhost:8080/combine?friendname=' + username + "&friendpassword=" + password);
		await page.waitForTimeout(7500);

		await browser.close();
	} catch(e) {
		console.error(e);
		try { await browser.close() } catch(e) {}
	}

}

module.exports = { queue, run }