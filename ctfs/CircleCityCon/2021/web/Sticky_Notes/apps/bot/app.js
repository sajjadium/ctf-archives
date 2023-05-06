import puppeteer from 'puppeteer'
import express from 'express'

const app = express()
const port = 3102
let browser

async function visit (url) {
  const ctx = await browser.createIncognitoBrowserContext()
  const page = await ctx.newPage()

  await page.setCookie({
    name: 'token',
    value: process.env.TOKEN,
    domain: '35.224.135.84',
    sameSite: 'strict',
    httpOnly: true
  })

  try {
    await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
    await page.waitForTimeout(10000)
  } finally {
    await page.close()
    await ctx.close()
  }
}

app.get('/visit/:id', async (req, res) => {
  const url = `http://35.224.135.84:3100/board/${req.params.id}`
  console.log(`[*] Visiting ${url}`)
  try {
    await visit(url)
    console.log(`[*] Done visiting ${url}`)
    res.sendStatus(200)
  } catch (e) {
    console.error(`[-] Error visiting ${url}: ${e.message}`)
    res.status(400).send({ error: e.message })
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
