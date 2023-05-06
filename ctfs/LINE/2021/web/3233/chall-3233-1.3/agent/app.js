const express = require('express')
const logger = require('morgan')
const puppeteer = require('puppeteer')
const process = require('process')
const axios = require('axios')

const flag = process.env.FLAG
const password = process.env.PASSWORD
const isDevelopment = process.env.NODE_ENV === 'development'
const host = isDevelopment ? 'localhost:13233' : 'front'

const app = express()

app.use(logger('dev'))

// setup
let browser
let mainPage

(async function setup () {
  // wait for server
  await new Promise((resolve) => {
    const id = setInterval(() => {
      axios.get(`http://${host}/api/users`).then(res => {
        if (res.status === 200) resolve(id)
      })
    }, 5 * 1000)
  }).then((id) => {
    clearInterval(id)
  })

  browser = await puppeteer.launch({
    executablePath: isDevelopment ? null : '/usr/bin/chromium-browser',
    args: [
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--window-size=500,1100'
    ],
    headless: !isDevelopment
  })

  // preparation of alice
  mainPage = await browser.newPage()
  mainPage.setViewport({
    width: 500,
    height: 1000
  })
  await mainPage.goto(`http://${host}/login`)
  await mainPage.type('input[type=text]', 'alice')
  await mainPage.type('input[type=password]', password)
  await Promise.all([
    mainPage.waitForNavigation({
      waitUntil: 'domcontentloaded',
      timeout: 10000
    }),
    mainPage.click('button')
  ])

  // preparation of bob
  await setupBob()

  // send the flag to bob every 30 seconds
  while (true) {
    await mainPage.close()
    mainPage = await browser.newPage()
    await mainPage.goto(`http://${host}/chat/bob`)
    await mainPage.type('textarea', flag)
    await mainPage.click('button')
    await sleep(30)
  }
})()

async function setupBob () {
  const context = await browser.createIncognitoBrowserContext()
  const bobPage = await context.newPage()
  await bobPage.goto(`http://${host}/login`)
  await bobPage.type('input[type=text]', 'bob')
  await bobPage.type('input[type=password]', password)
  await Promise.all([
    bobPage.waitForNavigation({
      waitUntil: 'domcontentloaded',
      timeout: 10000
    }),
    bobPage.click('button')
  ])
  await bobPage.close()
}

async function sleep (sec) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve()
    }, sec * 1000)
  })
}

module.exports = app
