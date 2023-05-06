const sleep = time => new Promise(resolve => setTimeout(resolve, time));

// not the actual admin bot script
// but basically the same :>
// npm install puppeteer
const puppeteer = require("puppeteer");

const BASE = "https://blogme.be.ax"
const FLAG = "corctf{test_flag}";

const USER = "test_user";
const PASS = "test_pass";

const visit = (id) => {
    let browser, page;
    return new Promise(async (resolve, reject) => {
        try {
            browser = await puppeteer.launch({
                headless: true,
                pipe: true,
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--js-flags=--noexpose_wasm'
                ],
                dumpio: true
            });

            page = await browser.newPage();
            await page.goto(BASE + "/api/login", {
                waitUntil: "networkidle2"
            });

            await page.evaluate((user, pass) => {
                document.querySelector("input[name=user]").value = user;
                document.querySelector("input[name=pass]").value = pass;
                document.querySelector("button[type=submit].btn-primary").click();
            }, USER, PASS);
            await page.waitForNavigation();

            await page.goto(BASE + "/post/" + id, {
                waitUntil: "networkidle2"
            });
            await page.waitForNavigation();

            await page.goto(BASE + "/api/comment/" + id, {
                waitUntil: "networkidle2"
            });

            let responses = [
                "wow!!!",
                "amazing!!!",
                "very cool!",
                "uhhh... okay?",
                ":lemonthink:",
                "cool i guess?",
                "why did you send me this?"
            ];
            let response = responses[Math.floor(Math.random()*responses.length)]
            response += " " + FLAG;

            await page.evaluate(response => {
                document.querySelector("textarea[name=text]").value = response;
                document.querySelector("button[type='submit'].btn-primary").click();
            }, response);
            await page.waitForNavigation();

            await page.close();
            page = null;
            await browser.close();
            browser = null;
        } catch (err) {
            console.log(err);
        } finally {
            if (page) await page.close();
            if (browser) await browser.close();
            resolve();
        }
    });
};

visit("post-id");