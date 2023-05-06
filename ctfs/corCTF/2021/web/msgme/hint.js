const sleep = time => new Promise(resolve => setTimeout(resolve, time));

// not the actual admin bot script
// but basically the same :>
// npm install puppeteer
const puppeteer = require("puppeteer");

const SITE = "https://msgme.be.ax";
const ADMIN_PASSWORD = "REDACTED";

const visit = (url) => {
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
            
            // yeah this is wack but idrc :))
            await page.evaluate((password, site) => {
                document.write(`
                    <form method="POST" action="${site}/chat/admin_login">
                        <input type="text" name="password" />
                        <input type="submit" />
                    </form>
                `);
                document.querySelector("input[name=password]").value = password;
                document.querySelector("input[type=submit]").click();
            }, ADMIN_PASSWORD, SITE);
            await sleep(3000);

            await page.goto(url);
            await sleep(14000);

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

visit("some url");