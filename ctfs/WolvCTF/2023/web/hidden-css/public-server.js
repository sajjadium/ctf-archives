const express = require('express')
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer')
const escape = require('escape-html')

const app = express()

app.use(express.static(__dirname + '/webapp'))
app.use(bodyParser.urlencoded({ extended: false }));

const visitUrl = async (url, cookieDomain) => {
    // Chrome generates this error inside our docker container when starting up.
    // However, it seems to run ok anyway.
    //
    // [0105/011035.292928:ERROR:gpu_init.cc(523)] Passthrough is not supported, GL is disabled, ANGLE is

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
            await page.setUserAgent('puppeteer');
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

app.post('/visit', async (req, res) => {
    const url = req.body.url
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

    try {
        console.log('visiting url: ', url)
        await visitUrl(url, req.hostname)
        res.send('Our evaluator has viewed your image!')
    } catch (e) {
        console.log('error visiting: ', url, ', ', e.message)
        res.send('Error visiting your URL: ' + escape(e.message))
    } finally {
        console.log('done visiting url: ', url)
    }
})

app.get('/', async (req, res) => {
    res.sendFile(__dirname + '/index.html')
})

const port = 8080
app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})