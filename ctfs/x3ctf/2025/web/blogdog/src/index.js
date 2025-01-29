const fs = require('fs')
const crypto = require('crypto');
const express = require('express');
const puppeteer = require("puppeteer");

const app = express();
const port = 3000;

const index = fs.readFileSync(__dirname + "/index.html").toString()

const FLAG = process.env?.FLAG || "x3c{this_is_a_fake_flag_1234567890_f4k3_fl4g_4lso_ure_4_qt_patootie}";
const COOLDOWN = 60*1000;
const TIMEOUT = 30*1000;

if (FLAG.length !== 68 || !/^x3c{[a-z0-9_]+}$/.test(FLAG)) throw Error("Invalid flag");

let last_request_time = 0;

app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  const nonce = crypto.randomBytes(16).toString('base64');  
  res.setHeader('Content-Type', 'text/html');
  res.setHeader('Content-Security-Policy', `script-src 'self' 'nonce-${nonce}'; style-src 'nonce-${nonce}'; object-src 'none'; img-src 'none';`);
  res.send(index.replaceAll("NONCE", nonce));
});

app.get('/purify.min.js', (req, res) => {
  res.sendFile(__dirname + "/purify.min.js");
});

app.get('/favicon.ico', (req, res) => {
  res.sendFile(__dirname + "/favicon.ico");
});

app.post('/', (req, res) => {
  let responseText = "Your response has been successfully recorded!\n"
  const content = (req?.body?.content || "").toString();
  const targetUrl = /https?:\/\/[^ ]*/.exec(content)?.[0];
  if (content) {
    if (Date.now() - last_request_time < COOLDOWN) {
      responseText = `Error: You can only submit 1 post a minute. Wait ${Math.floor((COOLDOWN - (Date.now() - last_request_time))/1000)} seconds.`;
    } else {
      responseText += "Note: Your post contained a link so we will check it to make sure it is safe.";
      last_request_time = Date.now();
      xssbot(targetUrl);
    }
  }
  res.send(responseText);
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
});

async function xssbot(url) {
  console.log(`Checking URL: ${url}`);
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    console.log(`URL does not start with 'http(s)://'`);
    return;
  }

  console.log("Launching browser");
  const browser = await puppeteer.launch({
      args: [
          '--headless',
          '--disable-dev-shm-usage',
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-gpu',
          '--no-gpu',
          '--disable-default-apps',
          '--disable-translate',
          '--disable-device-discovery-notifications',
          '--disable-software-rasterizer',
      ],
  });

  console.log(`Setting flag`);
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  await page.goto("http://localhost:3000/");
  await page.waitForSelector('#flag');
  await page.type('#flag', FLAG);

  console.log(`Opening ${url}`);
  setTimeout(() => {
    try {
      browser.close();
    } catch (err) {
      console.log(`Error: ${err}`);
    }
  }, TIMEOUT);
  try {
    await page.goto(url);
  } catch (err) {
    console.log(`Error: ${err}`);
  }
}
