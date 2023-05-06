const puppeteer = require('puppeteer-core');

const ADMIN_PASSWORD = process.env.PASSWORD || 'admin';
const LOGIN_PAGE = process.env.LOGIN_PAGE || 'https://0.0.0.0/login';

if (process.argv.length !== 4) {
  console.log(`Usage: node ${process.argv[1]} <url> <timeout>`);
  process.exit(1);
}

const url = process.argv[2];
const TIMEOUT_SECS = parseInt(process.argv[3] || '30', 10);

if (!url || url === '' || typeof(url) !== 'string') {
    console.log('No URL provided!');
    process.exit(1);
}

(async () => {
  // launch a browser with our config
  const browser = await puppeteer.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    IgnoreHTTPSErrors: true,
    args: [
      '--ignore-certificate-errors',
      // disable stuff we do not need
      '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage',
      // disable sandbox since it does not work inside docker
      // (but we will use seccomp at least)
      '--no-sandbox',
    ],
  });

  // open a new page
  console.log(`Logging in to ${LOGIN_PAGE}`)
  let page = await browser.newPage();
  await page.goto(LOGIN_PAGE);
  await page.type('#password', ADMIN_PASSWORD);
  await Promise.all([
    page.click("#submit"),
    page.waitForNavigation()
  ]);

  // avoid leaking anything
  await page.close();

  console.log('Opening new page');
  page = await browser.newPage();

  page.on('console', (msg) => {
    console.log('[Console]', msg);
  });

  // close the browser after TIMEOUT_SECS seconds
  setTimeout(() => browser.close(), TIMEOUT_SECS * 1000);

  // open the link
  console.log(`Visiting URL: ${url}`);
  await page.goto(url);
})().catch(error => {
  console.log('Error:', error);
  process.exit(1);
});
