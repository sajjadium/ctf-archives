const http = require("http");
const db = require("../db");
const puppeteer = require("puppeteer");

const browser_options = {
  headless: true,
  args: [
    "--no-sandbox",
    "--disable-background-networking",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-gpu",
    "--disable-sync",
    "--disable-translate",
    "--hide-scrollbars",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--js-flags=--noexpose_wasm,--jitless",
  ],
};

const visit = async (url) => {
  const port = process.env.PORT || 3000;
  try {
    const browser = await puppeteer.launch(browser_options);
    let context = await browser.createIncognitoBrowserContext();
    let page = await context.newPage(); 

    console.log("Admin logging in");
    await page.goto(`http://localhost:${port}/auth/login`);
    await page.waitForSelector("#username");
    await page.type("#username", process.env.ADMIN_USERNAME);
    await page.type("#password", process.env.ADMIN_PASSWORD);
    await page.click("#submit");
    await page.waitForTimeout(1000);
    // console.log(`Admin cookies are ${JSON.stringify(await page.cookies())}`);
    
    console.log(`Admin visiting url ${url}`);
    await page.goto(url, {
      waitUntil: "networkidle2",
      timeout: 5000,
    });
    // console.log(`Admin cookies are ${JSON.stringify(await page.cookies())}`);
    await page.waitForTimeout(3 * 1000);
    console.log("Everything okay, closing");
    page.close();
    context.close();
    await browser.close();
    return true;
  } catch (e) {
    console.log(e);
  }
  return false;
};

const urlSanity = (url) => {
  // TODO: Add real URL
  const port = process.env.PORT || 3000;
  const urlRegex = new RegExp(`^https?:\/\/localhost:${port}\/[a-zA-Z0-9\/]*$`);
  return url && urlRegex.test(url);
};

module.exports = {
  reportJob: async () => {
    const item = await db.fetchAndRemoveReport();
    if (item && item.id && urlSanity(item.url)) {
      // Authenticate and fetch the page
      return visit(item.url);
    }
  },
};
