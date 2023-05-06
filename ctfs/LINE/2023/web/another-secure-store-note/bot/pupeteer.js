const Puppeteer = require("puppeteer");
const { FLAG: flag } = process.env;

function sleep(time) {
    return new Promise((resolve) => {
        setTimeout(resolve, time);
    });
}

// Admin visiting your URL
async function visit(url) {
    const browser = await Puppeteer.launch({
        product: "firefox",
        headless: true,
        ignoreHTTPSErrors: true,
    });
    const page = await browser.newPage();
    const pageUrl = `https://${process.env.DOMAIN}:${process.env.PORT}`;

    await page.goto(pageUrl, { timeout: 3000, waitUntil: "domcontentloaded" });
    await page.type("#username", process.env.ADMIN_USERNAME);
    await page.type("#password", process.env.ADMIN_PASSWORD);
    await page.click("#submit");
    await sleep(500);

    await page.evaluate((flag) => {
        localStorage.setItem("secret", flag);
    }, flag); // Store flag to localStorage secret
    await page
        .goto(url, { timeout: 3000 })
        .catch((error) => console.error(error));
    await sleep(3000);
    await page.close();
    await browser.close();
}

module.exports = { visit };
