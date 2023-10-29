const puppeteer = require('puppeteer')

const FLAG = process.env.FLAG 
    ?? console.log('no FLAG set, use default')
    ?? 'flag{test}'

const APP_HOST = 'localhost'
const APP_PORT = 3000

const sleep = async (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const visit = async (url) => {
    console.log(`start: ${url}`)
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: '/usr/bin/google-chrome-stable',
        args: ['--no-sandbox'],
    })

    const ctx = await browser.createIncognitoBrowserContext();
    try{
        const page = await ctx.newPage();
        await page.setCookie({
            name: 'flag',
            value: FLAG,
            domain: `${APP_HOST}:${APP_PORT}`,
            httpOnly: true
        })
        await page.goto(url, {timeout: 5000})
        await sleep(3000)
        await page.close()
    }catch(e){
        console.log(e);
    }
    await ctx.close();
    await browser.close()
    console.log(`done: ${url}`)
}

module.exports.visit = visit