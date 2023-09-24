import { createClient } from "redis";
import puppeteer from "puppeteer";

const REDIS_URL = process.env["REDIS_URL"];
const TASK_URL = process.env["TASK_URL"];
const FLAG = process.env["FLAG"];

let browser = null;

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function visit(blogID) {
  console.log(`Visiting blog ${blogID}`);

  let context = null;
  try {
    if (!browser) {
      const args = [
        "--js-flags=--jitless,--no-expose-wasm",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--block-new-web-contents",
      ];

      browser = await puppeteer.launch({
        headless: "new",
        args,
      });
    }

    context = await browser.createIncognitoBrowserContext();

    const page1 = await context.newPage();
    await page1.goto(TASK_URL);
    await page1.waitForSelector("input#name");
    await page1.type("input#name", "An ordinary bot's blog");
    await Promise.all([page1.click("button"), page1.waitForNavigation()]);
    await page1.waitForSelector("input#title");
    await page1.type("input#title", "The Flag");
    await page1.type("textarea", FLAG);
    await page1.click("button");
    await sleep(2000);
    await page1.close();

    const page2 = await context.newPage();
    await page2.goto(`${TASK_URL}/blog/${blogID}`);
    await sleep(10000);
    await page2.close();
  } catch (e) {
    console.log(`Unexpected error: ${e}`);
  } finally {
    if (context) await context.close();
  }
}

async function main() {
  const client = await createClient({
    url: REDIS_URL,
  })
    .on("error", (err) => console.log(`Failed to connect to redis: ${err}`))
    .connect();

  await client.subscribe("blogs", visit);
}

main();
