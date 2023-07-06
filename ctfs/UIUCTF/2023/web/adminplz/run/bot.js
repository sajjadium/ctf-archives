const { chromium } = require('playwright-chromium');
const URL = process.argv[2];

(async () => {
    console.log('running admin bot...')
    const browser = await chromium.launch()
    const context = await browser.newContext()
    context.setDefaultTimeout(2000)
    const page = await context.newPage()
    await page.goto('http://127.0.0.1:8080/')

    // login
    await page.type('input[name=username]', 'admin')
    await page.type('input[name=password]', process.env.ADMIN_PASSWORD)
    await Promise.all([
      page.click('input[type=submit]'),
      page.waitForNavigation({
        waitUntil: 'networkidle0',
      }),
    ]);
    // visit url
    console.log("visiting target...");
    await page.goto(URL);
    await page.waitForTimeout(900000); // 15 min
    await browser.close()
    console.log('Success!')
})();

