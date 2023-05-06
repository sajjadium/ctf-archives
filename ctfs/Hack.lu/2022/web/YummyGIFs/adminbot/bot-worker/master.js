const puppeteer = require('puppeteer-core');

const TIMEOUT_SECS = parseInt(process.env.TIMEOUT_SECS || '30', 10);


if (process.argv.length !== 4) {
  console.log(`Usage: node ${process.argv[1]} <url> <loginJSON>`);
  process.exit(1);
}

const url = process.argv[2];
const { user, password, loginUrl, loginCheck } = JSON.parse(process.argv[3]) || {};

if (!url || url === '' || typeof (url) !== 'string') {
  console.log('No URL provided!');
  process.exit(1);
}

(async () => {
  // launch a browser with our config
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: [
      // disable stuff we do not need
      '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage',

      // disable sandbox since it does not work inside docker
      // (but we will use seccomp at least)
      '--no-sandbox',
    ],
  });

  // login
  console.log("logging in");
  let page = await browser.newPage();
  await page.goto(loginUrl);
  await page.type("#username", user);
  await page.type("#password", password);
  await Promise.all([
    page.click("#submit"),
    page.waitForNavigation()
  ]);
  const text = await page.content();
  if (!text.includes(loginCheck)) {
    throw Error("Not logged in!");
  }

  // avoid leaking anything
  console.log('Opening new page');
  await page.close();
  page = await browser.newPage();

  page.on('console', (msg) => {
    console.log('[Console]', msg);
  });

  // close the browser after TIMEOUT_SECS seconds
  setTimeout(() => browser.close(), TIMEOUT_SECS * 1000);

  // open the link
  console.log('Visiting URL');
  await page.goto(url);
})().catch(error => {
  console.log('Error:', error);
  process.exit(1);
});
