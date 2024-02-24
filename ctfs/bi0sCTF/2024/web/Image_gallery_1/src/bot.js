const puppeteer = require("puppeteer");
const fs = require("fs");


async function visit(flag_id,id) {
  const browser = await puppeteer.launch({
    args: [
        "--no-sandbox",
        "--headless"
    ],
    executablePath: "/usr/bin/google-chrome",
  });

  try {

    let page = await browser.newPage();

		await page.setCookie({
      
			httpOnly: true,
			name: 'sid',
			value: flag_id,
			domain: 'localhost',
      
		});

		page = await browser.newPage();

    await page.goto(`http://localhost:3000/`);

    await new Promise((resolve) => setTimeout(resolve, 3000));

    await page.goto(
      `http://localhost:3000/?f=${id}`,
      { timeout: 5000 }
    );

    await new Promise((resolve) => setTimeout(resolve, 3000));
    
    await page.close();
    await browser.close();

  } catch (e) {
    console.log(e);
    await browser.close();
  }
}

module.exports = { visit };