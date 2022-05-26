const puppeteer = require('puppeteer')

const LOGIN_URL = process.env.WEBAPP_URL + '/admin'
const ADMIN_PASSWORD = process.env.ADMIN_PWD

async function visit(url) {
    const browser = await puppeteer.launch({
        headless: true,
        args: [
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--no-sandbox',
            '--safebrowsing-disable-auto-update'
        ],
        executablePath: '/usr/bin/chromium'
    })


    try {
        let page = await browser.newPage()

        //login
        await page.goto(LOGIN_URL)

        await page.waitForSelector('#password')
        await page.focus('#password')
        await page.keyboard.type(ADMIN_PASSWORD, { delay: 10 })

        await new Promise(resolve => setTimeout(resolve, 300))
        await page.click('#submit')
        await new Promise(resolve => setTimeout(resolve, 300))

        //await page.waitForNavigation({ waitUntil: 'networkidle2' })
        //console.log(await page.cookies())

        // visit URL after auth
        await page.goto(url, { timeout: 5000 })
        await new Promise(resolve => setTimeout(resolve, 2000))

        // close browser
        await page.close()
        await browser.close()
    } catch (e) {
        console.log(e)
        await browser.close()
        //throw (e)
    }

}

module.exports = { visit }
