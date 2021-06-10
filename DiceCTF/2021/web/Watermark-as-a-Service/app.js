const dns = require("dns");
const express = require("express");
const ip = require("ip");
const path = require("path");
const puppeteer = require("puppeteer");
const sharp = require("sharp");
const { promisify } = require("util");

const resolve4 = promisify(dns.resolve4);

const app = express();

const ALLOWED_PROTOCOLS = ["http:", "https:"];
const BLOCKED_HOSTS = ["metadata.google.internal", "169.254.169.254"];

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname + "/public/index.html"));
});

const browser = puppeteer.launch({
  args: ["--no-sandbox", "--disable-setuid-sandbox"],
});

app.get("/snap", async (req, res) => {
  const url = decodeURIComponent(req.query.url);

  if (!url) {
    res.sendStatus(400);
    return;
  }

  let urlObj;
  try {
    urlObj = new URL(url);
  } catch {
    res.sendStatus(400);
    return;
  }

  const hostname = urlObj?.hostname;

  if (!hostname || ip.isPrivate(hostname)) {
    res.sendStatus(400);
    return;
  }

  if (BLOCKED_HOSTS.some((blockedHost) => hostname.includes(blockedHost))) {
    res.sendStatus(400);
    return;
  }

  const protocol = urlObj?.protocol;
  if (
    !protocol ||
    !ALLOWED_PROTOCOLS.some((allowedProtocol) =>
      protocol.includes(allowedProtocol)
    )
  ) {
    res.sendStatus(400);
    return;
  }

  let addresses
  try {
    addresses = await resolve4(hostname);
  } catch {
    res.sendStatus(400);
    return;
  }

  if (addresses.includes("169.254.169.254")) {
    res.sendStatus(400);
    return;
  }

  let ctx;
  try {
    ctx = await (await browser).createIncognitoBrowserContext();
    const page = await ctx.newPage();

    await page.goto(url);
    const imageBuffer = await page.screenshot();

    const outputBuffer = await sharp(imageBuffer)
      .composite([{ input: "dicectf.png", gravity: "southeast" }])
      .toBuffer()
    res.status(200).contentType("image/png").send(outputBuffer);
  } catch (error) {
    console.error(error);
    res.sendStatus(400);
    return;
  } finally {
    try {
      await ctx.close();
    } catch {}
  }
});

app.listen(3000, () => {
  console.log("Listening on 3000");
});

console.log(process.env.FLAG);
