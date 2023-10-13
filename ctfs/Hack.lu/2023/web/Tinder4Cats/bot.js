const puppeteer = require('puppeteer')
const crypto = require('crypto')

const TIMEOUT_SECS = parseInt(process.env.TIMEOUT_SECS || '30', 10)
const IDENTITY_DOMAIN = process.env.IDENTITY_DOMAIN || console.log('IDENTITY_DOMAIN missing Wtf')
const APP_DOMAIN = process.env.APP_DOMAIN || console.log('APP_DOMAIN missing Wtf')
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || console.log('ADMIN_USERNAME missing Wtf')
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || console.log('ADMIN_PASS missing Wtf')


if (process.argv.length !== 3 && process.argv.length !== 4) {
    console.log(`Usage: node ${process.argv[1]} <url> [cookies]`)
    process.exit(1)
  }

const url = process.argv[2]
const cookies = JSON.parse(process.argv[3] || '[]')

const setCookies = async (cookies, page) => {
    // set the cookies from json 
    for (const cookieSite of cookies) {
        console.log('[Cookie]', 'Visiting', cookieSite.url)
        await page.goto(cookieSite.url)
        console.log('[Cookie]', 'Setting cookies:', ...cookieSite.cookies)
        await page.setCookie(...cookieSite.cookies)
    }
}


if (!url || url === '' || typeof (url) !== 'string' || !url.startsWith('http') ) {
    console.log('No URL provided!')
    process.exit(1)
}

(async () => {
    // launch a browser with our config
    const browser = await puppeteer.launch({
        headless: 'new',
        executablePath: "/usr/bin/chromium-browser",
        args: [
            // disable stuff we do not need
            '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage',
            // disable sandbox since it does not work inside docker
            // (but we will use seccomp at least)
            '--no-sandbox',
            // no exploits please
            "--js-flags=--noexpose_wasm,--jitless",
        ],
    })

    // close the browser after TIMEOUT_SECS seconds
    setTimeout(() => {
        console.log('Timeout reached, closing browser')
        browser.close()
    }, TIMEOUT_SECS * 1000
    )

    // open a new page
    let page = await browser.newPage()

    // login 
    await page.goto(`https://${IDENTITY_DOMAIN}/login.php`, { waitUntil: 'networkidle0' })
    await page.type('#username', ADMIN_USERNAME)
    await page.type('#password', ADMIN_PASSWORD)
    // click and wait for navigation
    await Promise.all([
        page.click('#submit'),
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
    ])

    await page.goto(`https://${APP_DOMAIN}/login.php`, { waitUntil: 'networkidle0' })
    

    const client = await page.target().createCDPSession()
    await client.send('FedCm.enable')

    client.on('FedCm.dialogShown', async (event) => {
        console.log('[Dialog]', event)
        // select account 
        if (event.dialogType === 'AccountChooser'){
            await client.send('FedCm.selectAccount', {
                dialogId: event.dialogId,
                accountIndex: 0
            })
        }

    })

    await Promise.all([
        page.click('#fedcmbtn'),
        page.waitForNavigation({ waitUntil: 'networkidle0' }),
    ])

    // stop cdp 
    await client.send('FedCm.disable')
    client.detach()

    
    // avoid leaking anything
    await page.close()
    page = await browser.newPage()

    page.on('console', (msg) => {
        console.log('[Console]', msg)
    })

    // open the link
    console.log(`Visiting URL: ${url} `)
    await page.goto(`${url}`)
})().catch(error => {
    console.log('Error:', error)
    process.exit(1)
})
