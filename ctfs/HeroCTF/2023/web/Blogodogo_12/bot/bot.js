// required packages
const puppeteer = require("puppeteer");

// variables
const host = process.env.HOST;
const adminUsername = process.env.ADMIN_USERNAME;
const adminPassword = process.env.ADMIN_PASSWORD;

// sleep
const delay = (time) => {
    return new Promise(resolve => setTimeout(resolve, time));
}

// navigate
async function goto(url) {
	const browser = await puppeteer.launch({
		headless: true,
		ignoreHTTPSErrors: true,
		args: [ "--no-sandbox", "--ignore-certificate-errors" ],
		executablePath: "/usr/bin/chromium-browser"
	});

	const page = await browser.newPage();
	await page.setDefaultNavigationTimeout(5000);

    // Setup bot context
    await page.goto(host + "/login");
	const username = await page.waitForSelector("#username");
	const password = await page.waitForSelector("#password");
	await username.type(adminUsername);
	await password.type(adminPassword);
	await page.keyboard.press("Enter");
    await page.waitForNavigation();

    // Go to provided URL
	try {
	    await page.goto(url);
	} catch {}

    await delay(1000);

    browser.close();
	return;
}

if (process.argv.length === 2) {
    console.error("No URL provided!");
    process.exit(1);
}

goto(process.argv[2]);