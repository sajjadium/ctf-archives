const puppeteer = require('puppeteer');
const process = require('process')
const ADMIN_USERNAME = 'admin'
const ADMIN_PASSWORD = process.env.password
const FLAG = require('./config').FLAG
const view = async(url) => {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    })
    const page = await browser.newPage()
    await page.goto('http://localhost:8000/login')
    await page.type("#username", ADMIN_USERNAME)
    await page.type("#password", ADMIN_PASSWORD)
    await page.click('#btn-login')
        // get flag1
    await page.goto(url, { timeout: 5000 })
        // get flag2
    await page.setJavaScriptEnabled(false)
    await page.goto(url, { timeout: 5000 })
    await page.evaluate((url, FLAG) => {
        if (fff.lll.aaa.ggg.value == "this_is_what_i_want") {
            fetch(url + '?part2=' + btoa(encodeURIComponent(FLAG.substring(16))))
        } else {
            fetch(url + '?there_is_no_flag')
        }
    }, url, FLAG)
    await browser.close()
}

exports.view = view