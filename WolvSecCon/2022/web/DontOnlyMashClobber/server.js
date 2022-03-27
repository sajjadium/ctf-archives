const express = require('express')
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer')
const escape = require('escape-html')

const app = express()
const port = 80

app.use(express.static(__dirname + '/webapp'))
app.use(bodyParser.urlencoded({ extended: false }));

app.get('/personalize', (req, res) => {
    const imageUrl = req.query.image
    if (typeof imageUrl !== 'string' || !imageUrl) {
        res.send("'image' query parameter needs to be a string")
        return
    }

    try {
        new URL(imageUrl)
    }
    catch (e) {
        res.send(escape(e.message))
        return
    }

    const pageContent =
    `
        <html>
        <head>
            <script src="/app.js"></script>
        </head>
        <body id="body">
            <p>Here is the image you submitted:</p>
            <img id="user-image" src="${imageUrl}">
            <br/>
            <br/>
            <p>You submitted this url: <span id="user-image-info"></span></p>
        </body>
        </html>
    `

    // The intended solution does not involve bypassing CSP and gaining XSS.
    // If you can do so anyway, go for it! :)
    res.set("Content-Security-Policy", "default-src 'self'; img-src *; object-src 'none';")
    res.setHeader('Content-Type', "text/html")
    res.send(pageContent)
})

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

    if (parsedURL.hostname !== req.hostname) {
        res.send(`Please provide a URL with a hostname of: ${escape(req.hostname)}`)
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

app.listen(port, async () => {
    console.log(`Listening on ${port}`)
})