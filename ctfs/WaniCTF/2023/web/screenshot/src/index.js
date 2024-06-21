const playwright = require("playwright");
const express = require("express");
const morgan = require("morgan");

const main = async function () {
  const browser = await playwright.chromium.launch();

  const app = express();

  // Logging
  app.use(morgan("short"));

  app.use(express.static("static"));

  app.get("/api/screenshot", async function (req, res) {
    const context = await browser.newContext();
    context.setDefaultTimeout(5000);

    try {
      if (!req.query.url.includes("http") || req.query.url.includes("file")) {
        res.status(400).send("Bad Request");
        return;
      }

      const page = await context.newPage();

      const params = new URLSearchParams(req.url.slice(req.url.indexOf("?")));
      await page.goto(params.get("url"));

      const buf = await page.screenshot();

      res.header("Content-Type", "image/png").send(buf);
    } catch (err) {
      console.log("[Error]", req.method, req.url, err);
      res.status(500).send("Internal Error");
    } finally {
      await context.close();
    }
  });

  app.listen(80, () => {
    console.log("Listening on port 80");
  });
};

main();
