const net = require("net");
const crypto = require("crypto");
const puppeteer = require("puppeteer");

const APP_URL = process.env.APP_URL || process.exit(1);
const FLAG = process.env.FLAG || process.exit(1);
const PORT = process.env.PORT || process.exit(1);

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

  // Signup with random username/password
  await Promise.all([
    page1.waitForNavigation(),
    page1.goto(`${APP_URL}/signup`),
  ]);
  await page1.waitForSelector("#submit");
  await page1.type("#name", crypto.randomBytes(32).toString("hex"));
  await page1.type("#password", crypto.randomBytes(32).toString("hex"));
  await Promise.all([page1.waitForNavigation(), page1.click("#submit")]);

  // Create a note with the flag
  await page1.type("#note", FLAG);
  await Promise.all([page1.waitForNavigation(), page1.click("#addNote")]);

  await page1.close();

  const page2 = await context.newPage();
  try {
    await page2.goto(url, {
      timeout: 2000,
    });
    await sleep(120 * 1000);
  } catch (e) {
    console.log(e);
  }
  await page2.close();

  await context.close();
  await browser.close();

  console.log(`end: ${url}`);
};

const main = () => {
  const server = net.createServer((socket) => {
    socket.first = true;
    socket.on("data", async (data) => {
      try {
        if (socket.first) {
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
        }
      } catch (e) {
        console.log(e);
      }
    });
  });
  server.listen(PORT, () => {
    console.log("Started");
  });
};

main();
