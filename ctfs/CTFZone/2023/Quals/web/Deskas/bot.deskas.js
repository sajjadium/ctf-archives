import puppeteer from 'puppeteer'
import { nanoid } from 'nanoid'

const puppeter_args = {
  headless: 'old',
  args: [
    '--no-sandbox',
    '--user-data-dir=/tmp/chrome-userdata',
    '--breakpad-dump-location=/tmp/chrome-crashes',
    '--block-new-web-contents',
    '--disable-popup-blocking=false',
    '--enable-features=StrictOriginIsolation'
  ]
};

const VISIT_BLOG_TIMEOUT = 3000
const FLAG = process.env.FLAG || 'flag{redacted}'

const browser = await puppeteer.launch(puppeter_args);
const sleep = d => new Promise(r => setTimeout(r, d));

export default async function visit(url) {
  const context = await browser.createIncognitoBrowserContext();
  let page = await context.newPage({ ignoreSSL: true });

  await page.goto(url, { ignoreSSL: true })
  let pageStr = await page.evaluate(() => document.documentElement.innerHTML);

  await sleep(VISIT_BLOG_TIMEOUT)

  page = await context.newPage()
  await page.goto('https://deskas.ctfz.one/register')
  pageStr = await page.evaluate(() => document.documentElement.innerHTML);

  await page.focus('input[name=name]');
  await page.keyboard.type(nanoid(8))

  await page.focus('input[name=password]');
  await page.keyboard.type(nanoid(8))

  await page.waitForSelector('.register-container > button');
  await page.click('.register-container > button');

  await page.waitForSelector('.sites-container > button')
  await page.click('.sites-container > button')

  await page.waitForSelector('.site-form > input.site-name')
  await page.focus('.site-form > input.site-name')
  await page.keyboard.type(FLAG)

  await page.waitForSelector('.site-form > button')
  await page.click('.site-form > button')
}
