import puppeteer from "puppeteer";

const SERVER_URL = 'http://localhost:8081/chat';
const USERNAME = 'admin';

(async () => {
    const browser = await puppeteer.launch({
        headless: process.env.DEBUG ?? true
    });
    const page = await browser.newPage()
    await page.goto(SERVER_URL)
    await page.type('#username', USERNAME)
    await page.click('#btn-login')
    page.on('load', () => {
        console.log(page.url())
        if(page.url() !== SERVER_URL){
            setTimeout(async () => {
                await page.goto(SERVER_URL)
                await page.type('#username', USERNAME)
                await page.click('#btn-login')
            }, 3000);
        }
    })
})();