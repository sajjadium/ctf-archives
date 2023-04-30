const puppeteer = require("puppeteer")
const express = require("express")


const app = express()

app.get("/screenshot", (req, res) => {
  (async function () {

    try {
      const browser = await puppeteer.launch({
        headless: true,
        timeout: 60000,
        args: ['--no-sandbox']
      })
      const page = await browser.newPage()
      await page.setViewport({ width: 1920, height: 1080 })
      await page.goto('http://127.0.0.1/demo/inedx.jsp', { waitUntil: 'networkidle0' })
      const buffer = await page.screenshot({
        encoding: "binary",
        type: "png"
      })
      res.set("Content-Type", "image/png")
      res.send(buffer)
    } catch(err) {
      res.status(500).send(err.toString())
    }
  })()
})

app.listen(8090)
