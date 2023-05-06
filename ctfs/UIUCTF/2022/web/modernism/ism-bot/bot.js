/*
NOTE: this is the script that the admin bot runs to visit your provided URL
the same bot is used for the precisionism and modernism challenges
*/

const { chromium } = require('playwright-chromium');
const fs = require('fs');
const net = require('net');

// matches regex: ^uiuctf{[0-9A-Za-z]{8}}$
const FLAG1 = fs.readFileSync('/home/user/precisionism_flag.txt', {encoding: 'utf-8'}).trim();
// matches regex: ^uiuctf{[A-Za-z]+}$
const FLAG2 = fs.readFileSync('/home/user/modernism_flag.txt', {encoding: 'utf-8'}).trim();

(async function () {
  const browser = await chromium.launch({
    chromiumSandbox: true,
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
    const context = await browser.newContext({
      storageState: {
        cookies: [{
          name: "FLAG",
          value: FLAG1,
          domain: "precisionism-web.chal.uiuc.tf",
          path: "/",
          httpOnly: true,
          secure: true,
          sameSite: "None"
        },
        {
          name: "FLAG",
          value: FLAG2,
          domain: "modernism-web.chal.uiuc.tf",
          path: "/",
          httpOnly: true,
          secure: true,
          sameSite: "None"
        }]
      }
    });
    const page = await context.newPage();
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
    }, 10000);
  }

  var server = net.createServer();
  server.listen(1338)
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

