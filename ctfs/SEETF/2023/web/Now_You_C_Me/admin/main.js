import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.static('static'))
app.use(express.json())

const port = 80

async function visit(url) {

    const browser = await puppeteer.launch({
        dumpio: true,
        pipe: true,
        args: [
            '--js-flags=--jitless,--no-expose-wasm',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-features=BlockInsecurePrivateNetworkRequests' // Allow http://chall (https://chromestatus.com/feature/5436853517811712)
        ]
    })

    const ctx = await browser.createIncognitoBrowserContext()
    const page = await ctx.newPage()

    try {
        // Login to the app
        await page.authenticate({ 'username': process.env.USERNAME, 'password': process.env.PASSWORD })
        await page.goto('http://chall/api/health', { timeout: 5000, waitUntil: 'networkidle2' })

        // Go to your URL
        await page.goto(url, { timeout: 10000, waitUntil: 'networkidle2' })
        await page.waitForTimeout(10000)
    } finally {
        await page.close()
        await ctx.close()
    }

    await browser.close()
}

// app.use(
//     '/visit',
//     rateLimit({
//         windowMs: 60 * 1000,
//         max: 1, // 1 request per minute
//         message: { error: 'Too many requests, try again later' }
//     })
// )

app.post('/visit', async (req, res) => {
    const url = req.body.url
    if (
        url === undefined ||
        (!url.startsWith('http://') && !url.startsWith('https://'))
    ) {
        return res.status(400).send({ error: 'Invalid URL' })
    }

    try {
        console.log(`[*] Visiting ${url}`)
        await visit(url)
        console.log(`[*] Done visiting ${url}`)
        return res.sendStatus(200)
    } catch (e) {
        console.error(`[-] Error visiting ${url}: ${e.message}`)
        return res.status(400).send({ error: e.message })
    }
})

app.listen(port, async () => {
    console.log(`[*] Listening on port ${port}`)
})
