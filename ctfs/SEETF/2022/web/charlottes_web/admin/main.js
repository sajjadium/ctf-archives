import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.static('static'))
app.use(express.json())

const port = 8000

async function visit(url) {

    let browser = await puppeteer.launch({
        pipe: true,
        dumpio: true,
        headless: false,
        args: [
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--js-flags=--jitless',

            // Load vulnerable extension
            '--disable-extensions-except=/home/inmate/app/vuln/',
            '--load-extension=/home/inmate/app/vuln/'
        ]
    })

    // Admin successfully authenticates to the admin page before visiting your page.
    const prevPage = await browser.newPage()
    await prevPage.authenticate({ username: 'admin', password: process.env.SECRET })
    await prevPage.goto("http://app", { timeout: 5000, waitUntil: 'networkidle2' });

    const page = await browser.newPage()

    try {
        await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
        await page.waitForTimeout(5000)
    } finally {
        await page.close();
        await prevPage.close();
        await browser.close();
    }
}

app.use(
    '/visit',
    rateLimit({
        windowMs: 60 * 1000,
        max: 1,
        message: { error: 'Too many requests, try again later' }
    })
)

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
