import puppeteer from "puppeteer";

const FLAG = process.env.FLAG ?? "ping{FAKE}";

export const isValidUUID = (text) => {
	const uuidRegexp =
		/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

	return uuidRegexp.test(text);
};

export const report = async (data) => {
	if (!isValidUUID(data)) {
		throw new Error("Ivalid UUID format");
	}

	const browser = await puppeteer.launch({
		headless: "new",
		pipe: true,
		args: [
			"--disable-gpu",
			"--no-sandbox",
			"--js-flags=--noexpose_wasm,--jitless",
		],
		executablePath: "/usr/bin/chromium-browser",
	});

	const page = await browser.newPage();
	await page.setCookie({
		name: "FLAG",
		value: FLAG,
		domain: "localhost",
		path: "/",
	});

	await page.goto(`http://localhost:3000/result/${data}`);

	await new Promise((resolve) => setTimeout(resolve, 1000));

	await browser.close();
};
