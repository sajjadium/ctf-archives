const express = require('express')
const puppeteer = require('puppeteer')
const escape = require('escape-html')

const app = express()
const port = 80

app.use(express.static(__dirname + '/webapp'))

const visitUrl = async (url, cookieDomain) => {
    // Chrome generates this error inside our docker container when starting up.
    // However, it seems to run ok anyway.
    //
    // [0105/011035.292928:ERROR:gpu_init.cc(457)] Passthrough is not supported, GL is disabled, ANGLE is

    let browser =
            await puppeteer.launch({
                headless: true,
                pipe: true,
                dumpio: true,
                ignoreHTTPSErrors: true,

                // headless chrome in docker is not a picnic
                args: [
                    '--incognito',
                    '--no-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                ]
            })

    try {
        const ctx = await browser.createIncognitoBrowserContext()
        const page = await ctx.newPage()

        try {
            await page.setCookie({
                name: 'flag',
                value: process.env.FLAG,
                domain: cookieDomain,
                httpOnly: false,
                samesite: 'strict'
            })
            await page.goto(url, { timeout: 6000, waitUntil: 'networkidle2' })
        } finally {
            await page.close()
            await ctx.close()
        }
    }
    finally {
        browser.close()
    }
}

app.get('/visit', async (req, res) => {
    const url = req.query.url
    console.log('received url: ', url)

    let parsedURL
    try {
        parsedURL = new URL(url)
    }
    catch (e) {
        res.send(escape(e.message))
        return
    }

    if (parsedURL.protocol !== 'http:' && parsedURL.protocol != 'https:') {
        res.send('Please provide a URL with the http or https protocol.')
        return
    }

    if (parsedURL.hostname !== req.hostname) {
        res.send(`Please provide a URL with a hostname of: ${escape(req.hostname)}, your parsed hostname was: escape(${parsedURL.hostname})`)
        return
    }

    try {
        console.log('visiting url: ', url)
        await visitUrl(url, req.hostname)
        res.send('Our admin bot has visited your URL!')
    } catch (e) {
        console.log('error visiting: ', url, ', ', e.message)
        res.send('Error visiting your URL: ' + escape(e.message))
    } finally {
        console.log('done visiting url: ', url)
    }

})

app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})