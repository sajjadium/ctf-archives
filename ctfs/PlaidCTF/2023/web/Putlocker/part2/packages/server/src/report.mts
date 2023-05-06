import puppeteer from "puppeteer";

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD ?? "password";
const PUBLIC_HOST = process.env.PUBLIC_HOST ?? "client";
const PUBLIC_PORT = process.env.PUBLIC_PORT ?? "80";

export async function checkUrl(url: string) {
	if (!url.startsWith("http://") && !url.startsWith("https://")) {
		throw new Error("Invalid URL");
	}

	const browser = await puppeteer.launch({
		executablePath: "/usr/bin/chromium",
		headless: true,
		args: [
			"--no-sandbox",
			"--disable-setuid-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		]
	});

	try {
		console.log("[checkUrl] Logging in...");
		const loginPage = await browser.newPage();
		await loginPage.goto(`http://${PUBLIC_HOST}:${PUBLIC_PORT}/login`);
		await loginPage.type("input[placeholder='Username']", "admin");
		await loginPage.type("input[placeholder='Password']", ADMIN_PASSWORD);
		await loginPage.click("input[type='submit']");
		await new Promise((resolve) => setTimeout(resolve, 2000));
		await loginPage.close();

		console.log("[checkUrl] Going to " + url + "...");
		const page = await browser.newPage();
		await page.goto(url);
		await new Promise((resolve) => setTimeout(resolve, 10000));
		await page.close();
	} catch (error) {
		console.error("[checkUrl] Error: ", error);
		throw new Error("Failed to check URL");
	} finally {
		console.log("[checkUrl] Tearing down...");
		await browser.close();
	}
}