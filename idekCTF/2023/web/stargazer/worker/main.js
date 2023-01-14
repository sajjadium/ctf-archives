import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.static('static'))
app.use(express.json())
app.use(
    '/visit', rateLimit({
        windowMs: 30 * 1000,
        max: 10,
        message: { error: 'Too many requests, try again later' }
    })
)

const port = 7999
const domain_backend = "http://" + process.env.DOMAIN_BACKEND + ":1337/"
const domain_frontend = process.env.DOMAIN_FRONTEND || ""
const FLAG = process.env.FLAG || "FLAG{test_flag}"
let browser

async function visit(url) {
    // We only allow visiting backend.magic.world
    if (new URL(url).hostname !== 'backend.magic.world') {
        return;
    }

    const ctx = await browser.createIncognitoBrowserContext()
    const page = await ctx.newPage()
    try {

        await page.goto(domain_backend, { timeout: 2 * 1000, waitUntil: 'networkidle2' })
        await page.waitForNetworkIdle({idleTime: 1000, timeout: 2*1000})
        await page.setCookie({'name': "FLAG", "value": FLAG, "domain":".backend.magic.world"})

        await page.goto(url, { timeout: 2 * 1000, waitUntil: 'networkidle2' })
        await page.waitForNetworkIdle({idleTime: 20 * 1000})

    } catch (err){
        console.log(err);
    } finally {
        await page.close()
        await ctx.close()
    }

    console.log(`Done visiting -> ${url}`)
}

app.get('/visit', async (req, res) => {
    let {url} = req.query
    if(
        (typeof url !== 'string') || (url === undefined) || 
        (url === '') || (!url.startsWith(domain_backend))
    ){
        return res.status(400).send({error: "Invalid url"})
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
    browser = await puppeteer.launch({
        pipe: true,
        dumpio: true,
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-dev-shm-usage',
        ]
    })
    console.log(`[*] Listening on port ${port}`)
})
