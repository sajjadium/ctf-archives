import puppeteer from "puppeteer";
import Redis from "ioredis";

const crawl = async (url) => {
  console.log(`[*] started: ${url}`);

  const browser = await puppeteer.launch({
    product: "firefox",
    headless: true,
    ignoreHTTPSErrors: true,
  });
  const page = await browser.newPage();
  await page.setCookie({
    name: "uid",
    value: process.env.ADMIN_UID,
    domain: "app",
    expires: Date.now() / 1000 + 10,
  });

  await page
    .goto(url, {
      waitUntil: "load",
      timeout: 3000,
    })
    .catch((e) => {
      console.error(e);
    });

  await page.close();
  await browser.close();

  console.log(`[*] finished: ${url}`);
};

(async () => {
  const connection = new Redis(6379, "redis");
  while (true) {
    console.info("[*] waiting new query ...");
    const [err, message] = await connection.blpop("query", 0);
    if (message.startsWith("/")) {
      const url = `http://app:8080` + message;
      await crawl(url);
    } else {
      console.info(`[*] ignored: ${message}`);
    }
  }
})();
