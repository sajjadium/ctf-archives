const puppeteer = require("puppeteer");
const fs = require("fs");
const { random_bytes } = require("./utils");

const flag = fs.readFileSync("/flag.txt").toString();

async function visit(id, username) {
  const browser = await puppeteer.launch({
    args: ["--no-sandbox", "--headless"],
    executablePath: "/usr/bin/google-chrome",
  });
  try {
    let page = await browser.newPage();

    await page.goto(`http://localhost/login`);

    await page.waitForSelector("#username");
    await page.focus("#username");
    await page.keyboard.type(random_bytes(10), { delay: 10 });

    await page.waitForSelector("#password");
    await page.focus("#password");
    await page.keyboard.type(random_bytes(20), { delay: 10 });

    await new Promise((resolve) => setTimeout(resolve, 300));
    await page.click("#submit");
    await new Promise((resolve) => setTimeout(resolve, 300));

    page.setCookie({
      name: "FLAG",
      value: flag,
      domain: "localhost",
      path: "/",
      httpOnly: false,
      sameSite: "Strict",
    });

    await page.goto(
      `http://localhost/share/read#id=${id}&username=${username}`,
      { timeout: 5000 }
    );
    await new Promise((resolve) => setTimeout(resolve, 30000));
    await page.close();
    await browser.close();
  } catch (e) {
    console.log(e);
    await browser.close();
  }
}

module.exports = { visit };
