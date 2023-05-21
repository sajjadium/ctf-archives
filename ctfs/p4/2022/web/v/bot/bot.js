const net = require('net');
const { connect } = require('http2');
const puppeteer = require('puppeteer');
const Deque = require("double-ended-queue");
const fs = require('fs')

const XSSBOT_DOMAIN = process.env.XSSBOT_DOMAIN || 'bot';
const XSSBOT_PORT = process.env.XSSBOT_PORT || 1338;

const sleep = d => new Promise(r => setTimeout(r, d));

console.log(process.env);
const DOMAIN = process.env.DOMAIN || ".zajebistyc.tf";
const REGISTERED_DOMAIN = process.env.REGISTERED_DOMAIN;
const BLOCK_SUBORIGINS = process.env.BLOCK_SUBORIGINS == "1";
const BOT_TIMEOUT = process.env.BOT_TIMEOUT || 15000;
const MAX_BROWSERS = process.env.MAX_BROWSERS || 4;
const BOT_USER = process.env.BOT_USER || "duck";
const BOT_PASS = process.env.BOT_PASS || "zaq1@WSX";
const LOGIN_URL = process.env.LOGIN_URL || "http://nginx:3000/login";


async function visitUrl(browser, data, socket) {
  const { url, timeout: bot_timeout } = data;
  return new Promise(async resolve => {

    const context = await browser.createIncognitoBrowserContext();
    let page = await context.newPage();

    setTimeout(async () => {
      await context.close();
      resolve(1);
      socket_write(socket, 'Timeout\n');
      try {
        socket.destroy();
      } catch (err) {
        console.log(`err: ${err}`);
      }
    }, bot_timeout);

      try
      {
          await page.goto(url);
          await sleep(5000);
          await page.close();
          console.log(`visiting ${url} done, closed page`);

          // open new page to clear any XSS payloads before logging in
          page = await context.newPage();

          console.log("opening new page");
          await Promise.all([
              page.waitForNavigation({ waitUntil: 'load' }),
              page.goto(LOGIN_URL),
          ]);
          console.log("content loaded");
          await page.waitForSelector('#username');
          console.log('got selector');
          await page.$eval('#username', (el, val) => { el.value = val; }, BOT_USER);
          await page.$eval('#password', (el, val) => { el.value = val; }, BOT_PASS);
          await page.click('#submit');
          console.log("clicked");
          await sleep(5000);
          console.log(`visiting login done, closed page`);
      } catch(e) {
          console.log(`error: ${e}`);
      }
  });
}

class Queue {
  constructor(n_browsers) {
    this.browsers = [];
    this.queue = new Deque([]);
    this.addBrowsers(n_browsers);
    setInterval(() => { this.loop() }, 100);
  }
  async addBrowsers(N) {
    for (let i = 0; i < N; i++) {
      this.browsers[i] = {
        browser: await launchPup(i),
        free: true
      }
    }
  }

  add(socket, data) {
    this.loop();
    this.queue.push([socket, data]);
    console.log(`Adding ${data.url} to queue`);
    return this.queue.length;
  }

  loop() {
    for (let i = 0; i < this.browsers.length; i++) {
      if (this.queue.length === 0)
        break;
      if (this.browsers[i].free) {
        this.browsers[i].free = false;
        let [socket, data] = this.queue.shift();
        socket.state = 'LOADING';
        socket_write(socket, `Visiting: ${data.url}`);
        console.log(`Visiting ${data.url}`);
        visitUrl(this.browsers[i].browser, data, socket).finally(() => this.browsers[i].free = true);
      }
    }
  }

}

// will only be used if BLOCK_SUBORIGINS is enabled
const PAC_B64 = Buffer.from(`
function FindProxyForURL (url, host) {
  if (host == "${DOMAIN}") {
    return 'DIRECT';
  }
  if (host == "${REGISTERED_DOMAIN}" || dnsDomainIs(host, ".${REGISTERED_DOMAIN}")) {
    return 'PROXY 127.0.0.1:1';
  }
  return 'DIRECT';
}
`).toString('base64');

async function launchPup(i) {
  const r = i || Math.random() * 1e18;

  const puppeter_args = {
    headless: true,
    args: [
      `--user-data-dir=/tmp/chrome-userdata-${r}`,
      `--breakpad-dump-location=/tmp/chrome-crashes=${r}`,
      '--no-sandbox',// '--block-new-web-contents=true',
      '--enable-features=NetworkService',
      // '--unsafely-treat-insecure-origin-as-secure=http://postviewer:1337'
    ]
  };

  if (BLOCK_SUBORIGINS) {
    puppeter_args.headless = false;
    puppeter_args.args.push(
      '--proxy-pac-url=data:application/x-ns-proxy-autoconfig;base64,' + PAC_B64,
    )
  }
  return puppeteer.launch(puppeter_args);
}

function verifyUrl(data) {
  let url = data.toString().trim();
  let timeout = BOT_TIMEOUT;

  try {
    let j = JSON.parse(url);
    url = j.url;
    timeout = j.timeout;
  } catch (e) { }

  if (typeof url !== "string" || (!url.startsWith('http://') && !url.startsWith('https://'))) {
    return false;
  }
  return { url, timeout }
}

function socket_write(socket, data) {
  try {
    socket.write(data + '\n');
  }
  catch (e) { }
};

function ask_for_url(socket) {
  socket.state = 'URL';
  socket_write(socket, 'Please send me a URL to open.\n');
}

(async function () {
  const queue = new Queue(MAX_BROWSERS);

  async function load_url(socket, data) {
    data = verifyUrl(data);
    if (data === false) {
      socket.state = 'ERROR';
      socket_write(socket, 'Invalid scheme (http/https only).\n');
      socket.destroy();
      return;
    }

    socket.state = 'WAITING';

    const pos = queue.add(socket, data);
    socket_write(socket, `Task scheduled, position in the queue: ${pos}`);
  }

  const server = net.createServer();
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

    socket.on('error', e => {
      console.error(e);
    });

    try {
      ask_for_url(socket);
    } catch (err) {
      console.log(`err: ${err}`);
    }
  });
})();
