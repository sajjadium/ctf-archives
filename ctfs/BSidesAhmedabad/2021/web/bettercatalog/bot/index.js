const puppeteer = require("puppeteer");
const mysql = require("mysql");
const crypto = require("crypto");
const bcrypt = require("bcrypt");

const secret = "fakesecret";
const username = "admin_" + process.env["HOSTNAME"];
const password = crypto.createHmac("sha256", secret).update(process.env["HOSTNAME"]).digest("hex").substring(0, 24);

console.log(`Using credentials ${username}:${password}`);

function sleep(time) {
	return new Promise((resolve) => setTimeout(resolve, time));
}

async function run() {
	//Catalog is very insecure because of this extension, we are not goint to make that mistake again
	// let extension = "/ublock/uBlock0.chromium";
	let baseUrl = process.env.BASE_URL;

	while (true) {
		console.log("Setting up...");
		const browser = await puppeteer.launch({
			headless: false,

			executablePath: "/chrome-linux/chrome",
			args:[
				'--js-flags="--jitless --noexpose_wasm"', //hehe No ndayz
			]
		});

		try {
			console.log("\n".repeat(8));
			console.log("Opening page...");
			const page = await browser.newPage();
			await page.setViewport({ width: 1366, height: 768});

			console.log("Navigating...");
			await page.goto(baseUrl);
			console.log("Waiting for login...");
			await sleep(50);
			await page.waitForSelector(".login");
			await page.click(".login");
			await sleep(50);
			await page.type("input[name=username]", username);
			await page.type("input[name=password]", password);
			console.log("Submitting...");
			await Promise.all([
				page.click("button[value=login]"),
				page.waitForNavigation({ timeout: 5000, waitUntil: "networkidle2" })
			]);

			console.log("Done setting up for the next request, navigating to admin.php...");
			await page.goto(baseUrl + "/admin.php");

			if (await page.$("a.issue-pending-approval") === null) {
				console.log("No pending issue found, sleeping and reseting...");
				await sleep(10000);
			} else {
				console.log("About to click on the link!");
				page.on("request", (req) => console.log(req.url()));
				await Promise.all([
					page.click("a.issue-pending-approval"),
					page.waitForNetworkIdle({idleTime: 3000, timeout: 60000})


				]);
				console.log("RESOLVED");
				// console.log(await page.evaluate(() => document.body.innerHTML));
			}
		} catch (err) {
			console.error(err);
		} finally {
			await browser.close();
		}
	}
}

process.on("unhandledRejection", (e) => {
	throw e;
});

const connection = mysql.createConnection({
	host: process.env["MYSQL_HOST"],
	user: process.env["MYSQL_USER"],
	password: process.env["MYSQL_PASSWORD"],
	database: process.env["MYSQL_DATABASE"],
});

connection.connect((err) => {
	if (err) {
		throw err;
	}

	let pwhash = bcrypt.hashSync(password, 10);
	console.log(pwhash);

	connection.query("INSERT INTO user (username, password, is_admin) VALUES (?, ?, true) ON DUPLICATE KEY UPDATE username = username", [username, pwhash], (err, results) => {
		if (err) {
			throw err;
		}

		console.log(results);

		run();
	})
});
