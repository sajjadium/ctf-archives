const net = require("node:net");
const dns = require("node:dns").promises;
const puppeteer = require("puppeteer");

const FLAG = process.env.FLAG ?? console.log("No flag") ?? process.exit(1);
const PORT = process.env.PORT ?? "8000";
const APP_HOST = process.env.APP_HOST ?? "web";
const APP_PORT = process.env.APP_PORT ?? "3000";

if (!/^SECCON{[a-zA-Z0-9_]+}$/.test(FLAG)) {
  console.log("Bad flag");
  process.exit(1);
}

const sleep = async (msec) =>
  new Promise((resolve) => setTimeout(resolve, msec));

const visit = async (url) => {
  console.log(`start: ${url}`);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/usr/bin/google-chrome-stable",
    args: ["--no-sandbox"],
  });
  const context = await browser.createIncognitoBrowserContext();

  const page1 = await context.newPage();
  try {
    await page1.goto(`http://${APP_HOST}:${APP_PORT}`, { timeout: 1000 });
    await sleep(1 * 1000);
    await page1.waitForSelector("#content");
    await page1.type("#content", FLAG);
    await page1.waitForSelector("#create");
    await page1.click("#create");
    await sleep(1 * 1000);
  } catch (e) {
    console.log(e);
  }
  await page1.close();

  const page2 = await context.newPage();
  try {
    await page2.goto(url, {
      timeout: 2000,
    });
    await sleep(20 * 1000);
  } catch (e) {
    console.log(e);
  }
  await page2.close();

  await context.close();
  await browser.close();

  console.log(`end: ${url}`);
};

const main = async () => {
  const reportIp = (await dns.lookup(APP_HOST)).address;

  const server = net.createServer((socket) => {
    if (socket.remoteAddress !== reportIp) {
      socket.destroy();
      return;
    }

    socket.first = true;
    socket.on("data", async (data) => {
      try {
        if (!socket.first) return;
        socket.first = false;

        const url = data.toString().trim();
        if (url.startsWith("http://") || url.startsWith("https://")) {
          socket.write("Received :)");
          await visit(url);
        } else {
          socket.write("Bad url :(");
        }

        socket.end();
        socket.destroy();
      } catch (e) {
        console.log(e);
      }
    });
  });
  server.listen(PORT, "0.0.0.0", () => {
    console.log("Started");
  });
};

main();
