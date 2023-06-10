const puppeteer = require('puppeteer')

const url = process.env["URL"] || "http://proxed_proxy/";
const admin_secret = process.env["ADMIN_SECRET"] || "asd";

async function visit() {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] })

	try {
		var page = await browser.newPage()

		await page.setExtraHTTPHeaders({
			'authorization': admin_secret
		})
		await page.goto(url);
		await new Promise(resolve => setTimeout(resolve, 1000));

		await page.close()
		await browser.close()
		console.log("Bot alive")
	} catch (e) {
		await browser.close()
		console.log("Bot crashed :((")
	}
}

async function main() {
	while (1) {
		try{
			await visit();
		} catch(e){
			console.log("Unrecoverable error in last visit")
		}
		await new Promise(resolve => setTimeout(resolve, 1000));
	}
}

main()
.then(x => {
	console.error("Bot quit")
})