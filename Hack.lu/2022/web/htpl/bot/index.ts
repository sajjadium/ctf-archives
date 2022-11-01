import puppeteer, { Browser, Dialog, Page } from "puppeteer";
import express from "express";

const FLAG = process.env.FLAG || "flag{FAKE_FLAG}";

const app = express();

app.use(express.json());
let browser: Browser;

async function initBrowser() {
  browser = await puppeteer.launch({
    headless: true,
    args: ["--disable-gpu", "--no-sandbox"],
    executablePath: "/usr/bin/chromium-browser",
  });
}
async function testProgram(page: Page, program: string) {
  const base64Program = Buffer.from(program).toString("base64");
  const msgs: string[] = [];
  page.setCookie({
    name: "FLAG",
    value: FLAG,
    domain: "front",
  });
  await page.goto(`http://front:80/write.html#${base64Program}`, {
    waitUntil: "load",
  });

  page.on("dialog", (dialog: Dialog) => {
    msgs.push(dialog.message());

    dialog.dismiss().catch(() => {});
  });

  page
    .evaluate(() => {
      (window as any).run();
    })
    .catch(() => {});
  await page.waitForTimeout(1000);
  const output = msgs.join("\n");
  if (output) return `Nice program! Here is the output:\n\n${output}`;
  else return "WTF is going on? no output";
}

app.post("/api/submit", async (req, res) => {
  const program = `${req.body.program}`;

  const ctx = await browser.createIncognitoBrowserContext();
  const page = await ctx.newPage();
  try {
    const result = await testProgram(page, program);
    return res.send({ success: true, result });
  } catch (e) {
    console.error(e);
    return res.send({ success: false });
  } finally {
    page.close();
  }
});

app.listen(4000, async () => {
  await initBrowser();
  console.log("Bot ready, listening on port 4000");
});
