const puppeteer = require('puppeteer');
const execSync = require('child_process').execSync;
const crypto = require('crypto')

CHALL_URL = process.env.CHALL_URL ? process.env.CHALL_URL : "http://localhost:9011"
flag = process.env.FLAG ? process.env.FLAG : 'EPFL{fake_flag}'
latlon = process.env.LATLON ? process.env.LATLON : '46.520221,6.565842'

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
  }

async function play(page) { // admin accepts all challenges :)
    while (true) {
      try {
        await sleep(100)
        linkHandlers = await page.$x("//a[contains(text(), 'Click here to play!')]");
        if (linkHandlers.length > 0) {
        await linkHandlers[0].click();
        }
    } catch (e) {
    }
    }
}

async function botChallenge(username, premiumPin) {
    try {
        dataPath = "/tmp/"+crypto.randomBytes(16).toString('hex');
        execSync("cp -r ./profile "+dataPath)
        const browser = await puppeteer.launch({ headless: false, args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--js-flags=--noexpose_wasm,--jitless', '--use-fake-device-for-media-stream', '--use-fake-ui-for-media-stream', '--use-file-for-fake-video-capture=./happy.mjpeg','--user-data-dir='+dataPath] });
        const page = await browser.newPage();
        const context = browser.defaultBrowserContext()
        console.log(context)
        await page.setGeolocation({latitude:parseFloat(latlon.split(",")[0]), longitude:parseFloat(latlon.split(",")[1])})
        await page.goto(CHALL_URL);
        await page.waitForSelector('#registerLink')
        await sleep(100)
        await page.click('#registerLink');
        await page.waitForSelector('#homeBut')
        await sleep(100)
        await page.click('#homeBut');
        await sleep(100)
        await page.waitForSelector('#settingsLink')
        await sleep(100)
        await page.click('#settingsLink')
        await page.waitForSelector('#premiumPinInput')
        await sleep(100)
        await page.type('#premiumPinInput', premiumPin)
        await page.waitForSelector('#updateSettingsButton')
        await sleep(100)
        await page.click('#updateSettingsButton')
        await page.waitForSelector('#createNewChallBut')
        await sleep(100)
        await page.click('#createNewChallBut')
        await page.waitForSelector('#OpenLayersVersion')
        await sleep(100)
        await page.select('#OpenLayersVersion', '2.13')
        await page.waitForSelector('#winText')
        await sleep(100)
        await page.type('#winText', flag)
        await page.waitForSelector('#endMetadataButton')
        await sleep(100)
        await page.click('#endMetadataButton')
        await page.waitForSelector('#realBut')
        await sleep(100)
        await page.click('#realBut')
        await page.waitForSelector('#camerastartButton')
        await sleep(1000)
        await page.click('#camerastartButton')
        await sleep(2000)
        await page.waitForSelector('#captureButton')
        await sleep(100)
        await page.click('#captureButton')
        await page.waitForSelector('#confirmButton')
        await sleep(100)
        await page.click('#confirmButton')
        await page.waitForSelector('#usernameInput')
        await sleep(100)
        await page.type('#usernameInput', username)
        await page.waitForSelector('#challengeUserButton')
        await sleep(100)
        await page.click('#challengeUserButton')
        await sleep(1000)
        play(page)
        await sleep(60000)
        await browser.close();
    } catch (e) {
        console.log(e)
    }
}

module.exports = botChallenge
