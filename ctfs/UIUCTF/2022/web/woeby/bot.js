const { chromium } = require('playwright-chromium');
const { readFile }= require('node:fs/promises');

(async () => {
    console.log('reviewing submissions...')
    const browser = await chromium.launch()
    const context = await browser.newContext()
    context.setDefaultTimeout(2000)
    const page = await context.newPage()
    await page.goto('http://127.0.0.1/review/')

    // cheat to solve captcha... dont worry about it
    const phpsessid = (await context.cookies('http://127.0.0.1'))[0]['value']
    const sessData = await readFile(`/var/lib/php/sessions/sess_${phpsessid}`, 'utf8')
    const captcha = sessData.split('securimage_code_value|a:1:{s:7:"default";s:6:"')[1].substring(0,6)

    // login
    await page.fill('#user', 'admin')
    await page.fill('#pass', process.env.ADMIN_PASSWORD)
    await page.fill('input[name=captcha_code]', captcha)
    await page.click('#login')

    // do review!
    await page.locator('text=awaiting review').waitFor();
    // visit page
    await page.locator('a.tlink').last().click()
    await page.waitForTimeout(5000)
    // finish filling form
    await page.locator('input[name^=crawldepth]').last().fill('1')
    await page.locator('input[name^=crawlpages]').last().fill('5')
    await page.click('#submit')
    await browser.close()
    console.log('Success!')
})()
