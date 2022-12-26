const puppeteer = require('puppeteer');
const fs = require('fs');
const net = require('net');

const flag2 = 'nite{549387f2-00fc-4f70-a769-c8887f8dca65}'.repeat(1000); 
// don't worry about the exact flag, this is not the correct one,
// the correct one has the following regex nite{[a-zA-Z0-9_]+} and 
// a length of 36 chars. The flag is repeated a 1000 times.

const puppeter_args = {};
if (BLOCK_SUBORIGINS) {
  puppeter_args.headless = false;
  puppeter_args.executablePath = '/usr/bin/google-chrome-stable';
  puppeter_args.args = [
    '--disable-site-isolation-trials',
    '--user-data-dir=/tmp/chrome-userdata',
    '--breakpad-dump-location=/tmp/chrome-crashes'
  ];
}

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
    await page.goto( 'https://challenge.jsapi.tech/index.html' )
    await page.evaluate( function ( flag2) {
      window.localStorage.setItem( 'note', flag2 );
    }, flag2 );
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

