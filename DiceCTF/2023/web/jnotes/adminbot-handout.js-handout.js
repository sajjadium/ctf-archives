const fs = require('fs');
const puppeteer = require('puppeteer');

const flag = fs.readFileSync('./flag.txt', 'utf8').trim();

const challenge = {
  name: 'jnotes admin bot',
  urlRegex: /^https?:\/\/.*\//,
  timeout: 10000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    await page.goto('https://jnotes.mc.ax', { timeout: 3000, waitUntil: 'domcontentloaded' });
    await page.setCookie({
      name: "FLAG",
      value: flag,
      domain: "jnotes.mc.ax",
      path: "/",
      secure: true,
      httpOnly: true
    });

    console.log(`visiting url ${url}.`);
    await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' });
    await sleep(3000);
    console.log("done!")
  }
}

const sleep = time => new Promise(resolve => setTimeout(resolve, time))
const url = process.argv[2]
const regex = challenge.urlRegex ?? /^https?:\/\/.*/
if (!regex.test(url)) {
  throw new Error('invalid url')
}


(async () => {
  const browser = await puppeteer.launch({
    pipe: true,
    dumpio: true,
    args: ['--js-flags=--jitless', '--no-sandbox'],
  })
  const ctx = await browser.createIncognitoBrowserContext()
  console.log(`Starting...`);
  await Promise.race([
    challenge.handler(url, ctx),
    sleep(challenge.timeout),
  ]);
  await browser.close();
})();

