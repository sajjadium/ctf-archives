const puppeteer = require('puppeteer')
const crypto = require('crypto')

const PREMIUM_CODE = process.env.PREMIUM_CODE || 'PREMIUM'
const SSO_URL = process.env.SSO_URL || 'http://sso.localtest.me:3001'

const REGISTER_URL = `${SSO_URL}/register`
const LOGIN_URL = `${SSO_URL}/login`



async function visit(url) {
    const browser = await puppeteer.launch({
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
        ]
    })


    try {
        let page = await browser.newPage()


        //login
        await page.goto(REGISTER_URL)

        const u = crypto.randomBytes(20).toString('base64url')
        const p = crypto.randomBytes(20).toString('base64url')
        console.log(u,p)

        await page.waitForSelector('#username')
        await page.focus('#username')
        await page.keyboard.type(u)
        await page.focus('#password')
        await page.keyboard.type(p)
        await page.focus('#premium')
        await page.keyboard.type(PREMIUM_CODE)

        await Promise.all([
            page.waitForNavigation(),
            page.click('#submit')
        ])


        await page.goto(LOGIN_URL)

        await page.waitForSelector('#username')
        await page.focus('#username')
        await page.keyboard.type(u)
        await page.focus('#password')
        await page.keyboard.type(p)

        await Promise.all([
            page.waitForNavigation(),
            page.click('#submit')
        ])


        // visit URL after auth
        await page.goto(url,  {
            waitUntil: 'load'
        });

        await new Promise(resolve => setTimeout(resolve, 1000))

        // close browser
        await page.close()
        await browser.close()
    } catch (e) {
        console.error(e)
        await browser.close()
        //throw (e)
    }

}

module.exports = { visit }
