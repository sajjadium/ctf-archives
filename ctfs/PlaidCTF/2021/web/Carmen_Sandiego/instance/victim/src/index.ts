import puppeteer from "puppeteer";

const attackerUrl = process.env.ATTACKER_URL!;
const targetHost = process.env.TARGET_HOST!;
const adminPassword = process.env.ADMIN_PASSWORD!;

async function run() {
	const browser = await puppeteer.launch();
	const page = await browser.newPage();

	// Log in to the target site
	await page.goto(`http://${targetHost}/`);
	await page.type("[name=username]", "admin");
	await page.type("[name=password]", adminPassword);
	await Promise.all([
		page.click("[type=submit]"),
		page.waitForNavigation({ waitUntil: "networkidle2" })
	]);

	// Go to the attacker's URL
	await page.goto(attackerUrl);

	// Wait until we're killed by the runner...
}

run();
