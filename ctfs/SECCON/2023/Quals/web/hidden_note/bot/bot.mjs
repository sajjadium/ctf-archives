import puppeteer from "puppeteer";

const FLAG = process.env.FLAG ?? console.log("No flag") ?? process.exit(1);

const APP_HOST = "web";
const APP_PORT = "3000";
export const APP_URL = `http://${APP_HOST}:${APP_PORT}`;

if (!/^SECCON{[a-z0-9_]+}$/.test(FLAG)) {
  console.log("Bad flag");
  process.exit(1);
}

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

export const visit = async (url) => {
  console.log(`start: ${url}`);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox"],
  });

  const context = await browser.createIncognitoBrowserContext();

  try {
    // Create a flag note
    const page1 = await context.newPage();
    await page1.goto(APP_URL);
    await page1.waitForSelector("#content");
    await page1.type("#content", FLAG);
    await page1.waitForSelector("#create");
    await Promise.all([
      page1.click("#create"),
      page1.waitForNavigation({ timeout: 1000 }),
    ]);
    await page1.close();

    // Visit your URL
    const page2 = await context.newPage();
    await page2.goto(url, { timeout: 3 * 1000 });
    await sleep(60 * 1000);
    await page2.close();
  } catch (e) {
    console.error(e);
  }

  await context.close();
  await browser.close();

  console.log(`end: ${url}`);
};
