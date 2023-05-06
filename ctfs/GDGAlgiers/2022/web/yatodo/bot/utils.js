const puppeteer = require("puppeteer");

const browserOptions = {
  args: ["--no-sandbox"],
  headless: true,
};

const cookiesOptions = {
  name: "flag",
  value: process.env.FLAG,
  domain: process.env.CHALLENGE_HOST,
  path: "/",
  sameSite: "Strict",
};

const browse = async (url) => {
  try {
    const browser = await puppeteer.launch(browserOptions);
    const page = await browser.newPage();
    await page.setCookie(cookiesOptions);

    await page.goto(url, {
      waitUntil: "load",
      timeout: 5 * 1000,
    });
    await page.close();
    await browser.close();
  } catch (e) {
    console.log("Oops, something went wrong ", e);
  }
};

const isValidUrl = (str) => {
  let url;
  try {
    url = new URL(str);
  } catch {
    return false;
  }
  return url.protocol === "http:" || url.protocol === "https:";
};

module.exports = { browse, isValidUrl };
