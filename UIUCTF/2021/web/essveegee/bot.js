const { chromium } = require('playwright-chromium');

(async () => {
    const svgPath = process.argv[2].trim()
    const outPath = process.argv[3].trim()
    
    console.log('beginning conversion')
    const browser = await chromium.launch()
    const context = await browser.newContext({
        javaScriptEnabled: false
    })
    context.setDefaultTimeout(10000)

    const svgfile = svgPath.split('/').map((pathPart) => encodeURI(pathPart)).join('/')
    const page = await context.newPage()
    await page.goto('file://' + svgfile)
    const renderSettings = {
        path: outPath,
        type: 'png',
        omitBackground: true,
        fullPage: true
    }
    await page.waitForTimeout(60000)
    const svgEl = await page.waitForSelector('svg')
    await svgEl.screenshot(renderSettings)
    await browser.close()
})()