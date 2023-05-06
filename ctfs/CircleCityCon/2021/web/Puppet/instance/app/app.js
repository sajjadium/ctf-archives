import puppeteer from 'puppeteer'

const url = process.env.ATTACKER_URL
if (
  url === undefined ||
  (!url.startsWith('http://') && !url.startsWith('https://'))
) {
  console.error('Invalid attacker URL')
  process.exit(1)
}

const browser = await puppeteer.launch({
  dumpio: true,
  args: [
    '--disable-web-security',
    '--user-data-dir=/tmp/chrome',
    '--remote-debugging-port=5000',
    '--disable-dev-shm-usage', // Docker stuff
    '--js-flags=--jitless' // No Chrome n-days please
  ]
})

const ctx = await browser.createIncognitoBrowserContext()
const page = await ctx.newPage()

try {
  await page.goto(url)
  await page.waitForTimeout(15 * 1000)
} catch (e) {
  console.error(`[-] Error visiting ${url}: ${e.message}`)
} finally {
  await page.close()
  await ctx.close()
  await browser.close()
}
