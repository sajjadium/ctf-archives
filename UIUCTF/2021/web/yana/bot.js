/*
NOTE: this is the script that the admin bot runs to visit your provided URL
it not required to solve the challenge, but is provided for reference & for you to help test/debug your exploit
*/

const { chromium } = require('playwright-chromium');
const fs = require('fs');
const net = require('net');

const FLAG = fs.readFileSync('/flag.txt', {encoding: 'utf-8'});
// matches regex: uiuctf{[a-z0-9_]}

(async function () {
  const browser = await chromium.launch({
    executablePath: "/playwright/chromium-878941/chrome-linux/chrome",
    logger: {
      isEnabled: () => true,
      log: (name, severity, message, _args) => console.log(`chrome log: [${name}/${severity}] ${message}`)
    }
  });

  function ask_for_url(socket) {
    socket.state = 'URL';
    socket.write('Please send me a URL to open.\n');
  }

  async function load_url(socket, data) {
    let url = data.toString().trim();
    console.log(`checking url: ${url}`);
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      socket.state = 'ERROR';
      socket.write('Invalid scheme (http/https only).\n');
      socket.destroy();
      return;
    }
    socket.state = 'LOADED';

    // "incognito" by default
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto("https://chal.yana.wtf");
    await page.fill('#note > textarea', FLAG);
    await page.click('#note > button');
    await page.waitForTimeout(500);
    await page.goto('about:blank');
    await page.waitForTimeout(500);
    socket.write(`Loading page ${url}.\n`);
    await page.goto(url);
    setTimeout(() => {
      try {
        page.close();
        socket.write('timeout\n');
        socket.destroy();
      } catch (err) {
        console.log(`err: ${err}`);
      }
    }, 60000);
  }

  var server = net.createServer();
  server.listen(1338);
  console.log('listening on port 1338');

  server.on('connection', socket => {
    socket.on('data', data => {
      try {
        if (socket.state == 'URL') {
          load_url(socket, data);
        }
      } catch (err) {
        console.log(`err: ${err}`);
      }
    });

    try {
      ask_for_url(socket);
    } catch (err) {
      console.log(`err: ${err}`);
    }
  });
})();

