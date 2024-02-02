const puppeteer = require("puppeteer");
const fsp = require("fs/promises");
const os = require("os");

const FLAG = process.env.FLAG || "dice{test_flag}";

const tmpDir = `${os.tmpdir()}/safestlist`;
const launchBrowser = () => {
    return puppeteer.launch({
        headless: "new",
        pipe: true,
        args: [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--js-flags=--noexpose_wasm,--jitless",
        ],
        dumpio: true,
        executablePath: process.env.PUPPETEER_EXEC_PATH,
        userDataDir: tmpDir // so the note is still there after browser restart
    });
};

const sleep = ms => new Promise(r => setTimeout(r, ms));

const visit = async (url) => {
    // clear all data
    await fsp.rm(tmpDir, { recursive: true, force: true });

    let browser;
    try {
        browser = await launchBrowser();
        let page = await browser.newPage();

        // set flag
        await page.goto("http://localhost:3000", { timeout: 7500, waitUntil: "networkidle2" });
        await sleep(2000);
        await page.evaluate((flag) => {
            document.querySelector("input[type=text]").value = flag;
            document.querySelector("form[action='/create']").submit();
        }, FLAG);
        await page.waitForNavigation({ waitUntil: "networkidle2" });

        // restart browser, which should close all windows
        await browser.close();
        browser = await launchBrowser();
        page = await browser.newPage();

        // go to the submitted site
        await page.goto(url, { timeout: 7500, waitUntil: "networkidle2" })

        // restart browser, which should close all windows
        await browser.close();
        browser = await launchBrowser();
        page = await browser.newPage();

        // check on notes now that all other windows are closed
        await page.goto("http://localhost:3000", { timeout: 7500, waitUntil: "networkidle2" });
        await sleep(8000);
        await page.evaluate(() => {
            document.querySelector("form[action='/view']").submit();
        });
        await page.waitForNavigation({ waitUntil: "networkidle2" });
        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

module.exports = { visit };
