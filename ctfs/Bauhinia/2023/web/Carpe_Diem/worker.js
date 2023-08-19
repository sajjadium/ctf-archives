const puppeteer = require("puppeteer");
const crypto = require("crypto")
const PORT = process.env.PORT ?? 12345;
const FLAG = process.env.FLAG ?? "b6actf{THISISATESTFLAG}";
const flag_content = FLAG.slice(FLAG.indexOf("{") + 1, -1);
require("assert")(/^[A-Z]+$/.test(flag_content));

async function visit(url) {
    const browser = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome",
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--no-gpu',
            '--disable-default-apps',
            '--disable-translate',
            '--disable-device-discovery-notifications',
            '--disable-software-rasterizer',
            '--disable-xss-auditor'
        ],
        ignoreHTTPSErrors: true
    });
    const page = await browser.newPage();
    
    const idx = Math.floor(Math.random() * flag_content.length);
    const k = flag_content.charCodeAt(idx) - 65 + 1;

    for (let i = 0; i < k; i++) {
        await page.goto(`http://localhost:${PORT}/${crypto.randomBytes(20).toString("hex")}`, {waitUntil: "networkidle0"});
    }

    await page.goto(url+`?z=${idx}`, {waitUntil: "networkidle2"});
    await new Promise(r => setTimeout(r, 20000));
    await page.close();
    await browser.close();
}

module.exports = { visit };