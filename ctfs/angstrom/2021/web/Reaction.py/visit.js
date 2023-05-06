const puppeteer = require("puppeteer");
const fs = require("fs");

async function visit(username) {
    const browser = await puppeteer.launch({
        args: (process.env.CHROME_FLAGS || "").split`|`
    });
    const page = await browser.newPage();
    const dom = `127.0.0.1:8080`;
    await page.setCookie({
        name: "secret",
        value: fs.readFileSync("secret.txt", "utf8").trim(),
        httpOnly: true,
        sameSite: "Strict",
        domain: dom
    });
    await page.goto(`http://${dom}/?fakeuser=${encodeURIComponent(username)}`, {waitUntil: "networkidle2", timeout: 10000});
    await page.close();
    await browser.close();
}

if (process.argv[2]) {
    visit(process.argv[2]);
}
