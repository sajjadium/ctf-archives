import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.static('static'))
app.use(express.json())

const port = 8000
const APP_URL = 'http://app:80/'

let browser

async function visit(url) {

    browser = await puppeteer.launch({
        pipe: true,
        dumpio: true,
        args: [
            '--disable-dev-shm-usage',  // Docker stuff
            '--js-flags=--jitless'      // No Chrome n-days please
        ]
    })
    
    const appPage = await browser.newPage()
    
    // Admin stores the flag before visiting your URL
    await appPage.goto(APP_URL, { timeout: 5000, waitUntil: 'networkidle2' });
    await appPage.evaluate((flag, uuid) => {
        localStorage.setItem('note', flag);
        localStorage.setItem('uuid', uuid);
    }, process.env.FLAG, process.env.UUID);

    const userPage = await browser.newPage()
    try {
        await userPage.goto(url, { timeout: 120000, waitUntil: 'networkidle2' })
        await userPage.waitForTimeout(120000)
    } finally {
        await appPage.close()
        await userPage.close()
        await browser.close()
    }
}

app.use(
    '/visit',
    rateLimit({
        windowMs: 60 * 1000,
        max: 3,
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
