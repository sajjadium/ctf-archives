const crypto = require("crypto");
const fs = require("fs");
const net = require("net");
const puppeteer = require("puppeteer");

const wysiwygs = ["tinymce", "froala", "ckeditor"];

const flag = fs.readFileSync("/flag.txt").toString();

function xor(b1, b2) {
  if (b1.length != b2.length) {
    throw Error("buffers must be the same size");
  }
  const res = [];
  for (let i = 0; i < b1.length; i++) {
    res[i] = b1[i] ^ b2[i];
  }

  return Buffer.from(res);
}

async function generate_cookies(flag) {
  const flagLen = flag.length;
  const keys = [];
  let enc = Buffer.from(flag);

  for (let i of Array(wysiwygs.length - 1).keys()) {
    const key = crypto.randomBytes(flagLen);
    keys[i] = key;
    enc = xor(enc, key);
  }

  return [enc, ...keys].map(c => c.toString("hex"));
}

async function check_wysiwyg(browser, editor, cookie, data) {
  const text = data.toString().trim();
  const url = `http://web:5000/${editor}/`;

  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();
  await page.setCookie({ name: "key", value: cookie, url })



  try {
    await page.goto(
      `${url}?text=${text}`
    );
    await new Promise((resolve) => setTimeout(resolve, 5000));
  } catch (e) {
    console.log(e);
  }
  await page.close();
  await context.close();
}

async function start() {
  let browser;

  try {
    browser = await puppeteer.launch({ args: ["--no-sandbox"] });

    const server = net.createServer();
    server.listen(8000);

    server.on("connection", (socket) => {
      console.log("got connection");
      socket.on("data", async (data) => {
        try {
          if (socket.state == "waiting") {
            console.log("got data");


            socket.state = "running";
            socket.write("Admin is checking...");
            socket.end();
            socket.destroy();

            const cookies = await generate_cookies(flag);

            for (const [i, wysiwyg] of wysiwygs.entries()) {
              console.log("checking " + wysiwyg);
              await check_wysiwyg(browser, wysiwyg, cookies[i], data);
            }
          }
        } catch (err) {
          console.log(err);
        }
      });

      socket.state = "waiting";
    });
  } catch (err) {
    console.log(err);
    if (browser) {
      await browser.close();
    }
  }
}

start();
