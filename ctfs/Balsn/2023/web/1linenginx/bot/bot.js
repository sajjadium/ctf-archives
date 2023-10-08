const puppeteer = require('puppeteer')

const DOMAIN = process.env.DOMAIN || '1linenginx.balsnctf.com'
const FLAG = process.env.FLAG || 'BA1SN{fake}'

const sleep = async ms => new Promise(resolve => setTimeout(resolve, ms))

let browser = null

const visit = async url => {
    let context = null
    try {
        if (!browser) {
            const args = ['--js-flags=--jitless,--no-expose-wasm', '--disable-gpu', '--disable-dev-shm-usage']
            browser = await puppeteer.launch({
                headless: 'new',
                args
            })
        }

        context = await browser.createIncognitoBrowserContext()
        const page = await context.newPage()

        await page.setCookie({name: 'flag', value: FLAG, domain: DOMAIN});

        await page.goto(url)
        await page.bringToFront()
        await sleep(5000)
        await page.close()

        await context.close()
        context = null
    } catch (e) {
        console.log(e)
    } finally {
        if (context) await context.close()
    }
}

module.exports = visit

if (require.main === module) {
    visit('http://example.com')
}
