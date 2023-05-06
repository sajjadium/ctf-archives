import puppeteer from "puppeteer";

const attackerUrl = process.env.ATTACKER_URL!;
const targetHost = process.env.TARGET_HOST!;
const adminPassword = process.env.ADMIN_PASSWORD!;

async function run() {
	const browser = await puppeteer.launch();
	let page = await browser.newPage();

	// Log in to the target site
	await page.goto(`http://${targetHost}/`);
	await page.type("[name=username]", "admin");
	await page.type("[name=password]", adminPassword);
	await Promise.all([
		page.click("[type=submit]"),
		page.waitForNavigation({ waitUntil: "networkidle2" })
	]);
	await page.close();

	page = await browser.newPage();
	// Go to the attacker's URL
	if (attackerUrl.startsWith("http://") || attackerUrl.startsWith("https://")) {
		await page.goto(attackerUrl);
	}

	// Wait until we're killed by the runner...
}

run();
