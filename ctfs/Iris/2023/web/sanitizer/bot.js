const puppeteer = require('puppeteer');
const fs = require('fs');
const net = require('net');

const BOT_TIMEOUT = process.env.BOT_TIMEOUT || 60*1000;

const puppeter_args = {"args": [
    '--no-sandbox',
    `--window-size=1920,1080`,
    '--window-position=0,0',
    '--hide-scrollbars',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding'], headless: true};

(async function(){
  const browser = await puppeteer.launch(puppeter_args);

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

    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();
    await page.goto("https://sanitizer-web.chal.irisc.tf/");
    let flag = fs.readFileSync('/home/user/flag').toString().trim();
    await page.evaluate(`window.localStorage['flag'] = '${flag}'`);
    socket.write(`Loading page ${url}.\n`);
    setTimeout(()=>{
      try {
        context.close();
        socket.write('timeout\n');
        socket.destroy();
      } catch (err) {
        console.log(`err: ${err}`);
      }
    }, BOT_TIMEOUT);
    await page.goto(url);
  }

  var server = net.createServer();
  server.listen(1338);
  console.log('listening on port 1338');

  server.on('connection', socket=>{
    socket.on('data', data=>{
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

