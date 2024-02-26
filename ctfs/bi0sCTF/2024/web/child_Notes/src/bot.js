const puppeteer = require("puppeteer");

async function visit(uid, user, admin_pass) {
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/chromium-browser",
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  try {
    const url = `http://localhost:8000/verify?uid=${uid}&user=${user}`;
    console.log(`Visiting ${url}`);
    const page = await browser.newPage();
    await page.goto("http://localhost:8000/login");
    await page.type('input[id="logusername"]', "admin");
    await page.type('input[id="logpassword"]', admin_pass);
    await page.click('button[id="log"]');
    await page.waitForSelector("#q");
    await page.goto(url, { waitUntil: "networkidle0", timeout: 60000 });
    await page.close();
  } catch (err) {
    console.log(`Error in visit: ${err}`);
  }
  try {
    await browser.close();
    console.log("Browser closed");
  } catch (e) {
    console.log("Closing browser failed.");
  }
}
module.exports = { visit: visit };
