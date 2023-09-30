import puppeteer from 'puppeteer'
import express from 'express'

const app = express()
app.use(express.json())

const port = 80
let browser

async function visit (url) {
  const ctx = await browser.createIncognitoBrowserContext()
  const page = await ctx.newPage()

  try {
    url = new URL(url)
    url.searchParams.append('token', process.env.JUPYTER_TOKEN)
    console.log(`[*] Visiting ${url}`)
    await page.goto(url.toString(), { timeout: 5000, waitUntil: 'networkidle2' })
    await page.waitForTimeout(parseInt(process.env.BOT_TIMEOUT || '10000'))

    await page.evaluate(() => window.IPython.notebook.close_and_halt())

    console.log(`[*] Done visiting ${url}`)
  } finally {
    await page.close()
    await ctx.close()
  }
}

app.post('/visit', async (req, res) => {
  const token = req.body.token
  console.log(token)
  console.log(process.env.BOT_TOKEN)
  if (token === undefined || token !== process.env.BOT_TOKEN) {
    return res.sendStatus(403)
  }

  const url = req.body.url
  if (
    url === undefined ||
    (!url.startsWith('http://') && !url.startsWith('https://'))
  ) {
    return res.status(400).send({ error: 'Invalid URL' })
  }

  try {
    await visit(url)
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
    args: [
      '--disable-dev-shm-usage', // Docker stuff
      '--js-flags=--jitless' // No Chrome n-days please
    ]
  })
  console.log(`[*] Listening on port ${port} ...`)
})
