import puppeteer from 'puppeteer'
import { createClient } from 'redis'

async function crawl(path) {
    if (!path.startsWith('/')) {
        return
    }
    const targetUrl = `http://${process.env.APP_DOMAIN}:${process.env.APP_PORT}${path}`

    const browser = await puppeteer.launch({
        executablePath: 'google-chrome-stable',
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-background-networking',
            '--disk-cache-dir=/tmp',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
        ]
    })
    const page = await browser.newPage()
    page.setCookie({
        name: 'cookie',
        value: process.env.FLAG,
        domain: process.env.APP_DOMAIN
    })
    await page.setExtraHTTPHeaders({
        // For CTF players: just ignore this line.
        'Bypass-Tunnel-Reminder': 'true',
    });
    await page.goto(targetUrl, {
        waitUntil: 'load',
        timeout: 10000
    })
    await page.close()
    await browser.close()
}

const client = createClient({
    url: process.env.REDIS_REPORTER_URL
})

await client.connect()

while (true) {
    console.log('[*] waiting new query...')
    const { element: path } = await client.blPop('query', 0)
    await crawl(path)
    console.log(`[*] proceeded: ${path}`)
    await client.incr('proceeded_count')
}
