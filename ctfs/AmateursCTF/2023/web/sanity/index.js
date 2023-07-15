import express from "express";
import bodyParser from "body-parser";
import { nanoid } from "nanoid";
import path from "path";
import puppeteer from "puppeteer";

const sleep = (ms) => new Promise((res) => setTimeout(res, ms));

const __dirname = path.resolve(path.dirname(""));
const app = express();
const port = 3000;

app.set("view engine", "ejs");
app.use(bodyParser.json());

const browser = puppeteer.launch({
  pipe: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});
const sanes = new Map();

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, `/index.html`));
});

app.post("/submit", (req, res) => {
  const id = nanoid();
  if (!req.body.title) return res.status(400).send("no title");
  if (req.body.title.length > 100)
    return res.status(400).send("title too long");
  if (!req.body.body) return res.status(400).send("no body");
  if (req.body.body.length > 2000) return res.status(400).send("body too long");

  sanes.set(id, req.body);

  res.send(id);
});

app.get("/:sane", (req, res) => {
  const sane = sanes.get(req.params.sane);
  if (!sane) return res.status(404).send("not found");

  res.render("sanes", {
    id: req.params.sane,
    title: encodeURIComponent(sane.title),
    body: encodeURIComponent(sane.body),
  });
});

app.get("/report/:sane", async (req, res) => {
  let ctx;
  try {
    ctx = await (await browser).createIncognitoBrowserContext();
    const visit = async (browser, sane) => {
      const page = await browser.newPage();
      await page.goto("http://localhost:3000");
      await page.setCookie({ name: "flag", value: process.env.FLAG });
      await page.goto(`http://localhost:3000/${sane}`);
      await page.waitForNetworkIdle({ timeout: 5000 });
      await page.close();
    };

    await Promise.race([visit(ctx, req.params.sane), sleep(10_000)]);
  } catch (err) {
    console.error("Handler error", err);
    if (ctx) {
      try {
        await ctx.close();
      } catch (e) {}
    }
    return res.send("Error visiting page");
  }
  if (ctx) {
    try {
      await ctx.close();
    } catch (e) {}
  }
  return res.send("Successfully reported!");
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
