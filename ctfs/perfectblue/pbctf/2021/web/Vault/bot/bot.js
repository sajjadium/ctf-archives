const crypto = require("crypto");
const net = require("net");
const puppeteer = require("puppeteer");

const vaultUrl = process.env.VAULT_URL || "http://web:5000/";
const FLAG = process.env.FLAG || "ctf{not_the_flag}";

async function click_vault(page, i) {
  const vault = `a.vault-${i}`;
  const elem = await page.waitForSelector(vault, { visible: true });
  await Promise.all([page.waitForNavigation(), elem.click()]);
}

async function add_flag_to_vault(browser, url) {
  if (!url || url.indexOf("http") !== 0) {
    return;
  }
  const page = await browser.newPage();

  try {
    await page.goto(vaultUrl);

    for (let i = 0; i < 14; i++) {
      await click_vault(page, crypto.randomInt(1, 33));
    }
    await page.type("#value", FLAG);
    await Promise.all([page.waitForNavigation(), page.click("#submit")]);

    await page.goto(url);
    await new Promise((resolve) => setTimeout(resolve, 30 * 1000));
  } catch (e) {
    console.log(e);
  }
  await page.close();
}

async function start() {
  try {
    const server = net.createServer();
    server.listen(8000);

    server.on("connection", async (socket) => {
      const browser = await puppeteer.launch({
        args: ["--no-sandbox"],
        headless: false,
      });
      console.log("got connection");
      socket.on("data", async (data) => {
        try {
          if (socket.state == "waiting") {
            console.log("got data");

            socket.state = "running";
            socket.write("Admin is checking...");
            socket.end();
            socket.destroy();

            await add_flag_to_vault(browser, data.toString().trim());
          }
        } catch (err) {
          console.log(err);
        } finally {
          await browser.close();
        }
      });

      socket.state = "waiting";
    });
  } catch (err) {
    console.log(err);
  }
}

start();
