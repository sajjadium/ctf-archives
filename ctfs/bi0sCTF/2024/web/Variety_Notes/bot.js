const puppeteer = require("puppeteer");

async function visit(title, note, admin_pass) {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--headless"],
    executablePath: "/usr/bin/google-chrome",
    headless: "new",
  });
  try {
    const authUser = process.env.INSTANCE_USERNAME || "admin";
    const authpass = process.env.INSTANCE_PASSWORD || "password";
	  console.log(`bot username ${authUser} and password ${authpass}`);
    const appUrl =
      process.env.INSTANCE_IP && process.env.INSTANCE_PORT
        ? process.env.INSTANCE_IP + process.env.INSTANCE_PORT + "/"
        : "http://localhost:3000/";
	  console.log(appUrl);
	  const page = await browser.newPage();

    await page.authenticate({
      username: authUser,
      password: authpass,
    });

    await page.goto(appUrl);
    await page.type('input[name="username"]', "admin");
    await page.type('input[name="password"]', admin_pass);
    await page.click('button[type="submit"]');

    await page.goto(appUrl);
    await page.type('input[name="title"]', title);
    await page.type('textarea[name="note"]', note);
    await page.click('button[name="create"]');
    await page.waitForNavigation();

    await page.waitForTimeout(5000);

    await browser.close();
  } catch (error) {
    console.error("Error:", error);
  }
  try {
    await browser.close();
    console.log("Browser Closed");
  } catch (e) {
    console.log(e);
  }
}

module.exports = { visit };
