import puppeteer from "puppeteer";
import { readFileSync } from "fs";
import { adminCookie } from "./app.js";

const FLAG = readFileSync("./flag.txt", "utf-8").trim();

export const report = async (endpoint) => {
	if (!endpoint.startsWith("?text=")) {
		throw new Error(
			"Invalid endpoint. Make sure to have the 'text' query parameter."
		);
	}

	const browser = await puppeteer.launch({
		headless: "new",
		args: [
			"--disable-gpu",
			"--no-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		],
		executablePath: "/usr/bin/chromium-browser",
	});

	const page = await browser.newPage();
	await page.setCookie({
		name: "admin",
		value: adminCookie,
		domain: "localhost",
		path: "/",
		httpOnly: true,
	});

	await page.setCookie({
		name: "flag",
		value: FLAG,
		domain: "localhost",
		path: "/",
	});

	await page.goto(`http://localhost:3000/${endpoint}`);

	await new Promise((resolve) => setTimeout(resolve, 1000));

	await browser.close();
};
