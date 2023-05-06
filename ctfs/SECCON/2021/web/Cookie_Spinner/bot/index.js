const net = require("net");
const puppeteer = require("puppeteer");

const APP_HOST = process.env.APP_HOST || process.exit(1);
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

  const page = await context.newPage();
  page.setCookie({
    name: "cookie",
    value: FLAG,
    domain: APP_HOST,
  });

  try {
    await page.goto(url, {
      timeout: 2000,
    });
    await sleep(10 * 1000);
  } catch (e) {
    console.log(e);
  }

  await page.close();
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
