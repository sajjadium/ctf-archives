const puppeteer = require("puppeteer");
const crypto = require("crypto");

const generate = async (url) => {
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--js-flags=--noexpose_wasm,--jitless' // this is a web chall :>
        ],
        dumpio: true,
        pipe: true, // lmao no
        executablePath: process.env.PUPPETEER_EXEC_PATH
    });

    const page = await browser.newPage();

    await page.goto(url, { waitUntil: "networkidle0" });

    const pdf = `${crypto.randomUUID()}.pdf`;

    await page.pdf({ path: `./output/${pdf}` });

    await browser.close();

    return pdf;
};

module.exports = { generate };