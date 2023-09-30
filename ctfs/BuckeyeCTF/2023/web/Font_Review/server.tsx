import { Elysia, t } from "elysia";
import { html } from "@elysiajs/html";
import * as csstree from "css-tree";
import puppeteer from "puppeteer";

const SuccessMessageComponent = () => {
  const successMessages = [
    "Ohh nice glyphs!",
    "I love your kerning!",
    "Wow, your font choice is exquisite!",
    "Your typography skills are top-notch!",
    "I'm impressed with your typeface selection!",
    "The ligatures in your font are fantastic!",
    "Your leading and line spacing are on point!",
    "Kudos on the elegant serifs in your font!",
    "The balance in your typography is impeccable!",
    "Your font's readability is superb!",
    "Great job on the character spacing in your font!",
    "Your font has a wonderful sense of style!",
    "I can tell you put a lot of thought into your font design!",
    "The weight variations in your font are delightful!",
    "Your font is a true work of art!",
    "I'm loving the letterforms in your font!",
    "The details in your typeface are impressive!",
  ];

  return (
    <>
      <div style="margin-bottom: 1em">🎉 Amazing! 🎉</div>
      <div>
        {successMessages[Math.floor(Math.random() * successMessages.length)]}
      </div>
    </>
  );
};

const ErrorMessageComponent = () => {
  const constructiveCriticismMessages = [
    "I think your kerning could use some improvement.",
    "The readability of your font might need some attention.",
    "The character spacing in your font could be refined.",
    "Your font's x-height seems a bit inconsistent.",
    "The serifs in your typeface could be more refined.",
    "Consider enhancing the contrast in your font's weights.",
    "The ligatures in your font might benefit from refinement.",
    "Your font's baseline appears slightly uneven.",
    "The italics in your typeface could use some refinement.",
    "The descenders in your font seem a bit too long.",
    "The ascenders in your font could be more consistent.",
    "Consider working on the legibility of your font at smaller sizes.",
    "Your font's uppercase and lowercase letters need better harmony.",
    "The overall style of your font needs more coherence.",
    "I suggest revisiting the spacing between certain letter pairs.",
    "The overall texture of your font could use some improvement.",
  ];

  return (
    <>
      <div style="margin-bottom: 1em">🤔 Feedback 🤔</div>
      <div>
        {
          constructiveCriticismMessages[
            Math.floor(Math.random() * constructiveCriticismMessages.length)
          ]
        }
      </div>
    </>
  );
};

const app = new Elysia()
  .use(html())
  .get("/styles.css", () => Bun.file("styles.css"))
  .get("/", () => (
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Font Review</title>
        <link
          href="https://fonts.googleapis.com/css?family=Roboto+Mono"
          rel="stylesheet"
        />
        <link href="/styles.css" rel="stylesheet" />
      </head>
      <body>
        <div class="content">
          <h3>Send me your font to review!</h3>
          <form method="POST">
            <input
              type="text"
              name="url"
              placeholder="https://your-cdn.tld/your-font"
              style={{ marginRight: "1em", width: "500px" }}
            />
            <button type="submit" class="review-button">
              Review
            </button>
          </form>
        </div>
      </body>
    </html>
  ))
  .post(
    "/",
    async ({ body }) => {
      const css = `@font-face {\nfont-family: content;\nsrc: url(${body.url})}`;
      const ast = csstree.parse(css);
      const fontFaceRules: csstree.Atrule[] = [];
      csstree.walk(ast, {
        visit: "Atrule",
        enter: (node) => {
          if (node.name === "font-face") {
            fontFaceRules.push(node);
          }
        },
      });

      if (fontFaceRules.length === 0) {
        throw new Error("No @font-face rules provided!");
      }

      const fontFaceCss = fontFaceRules
        .map((rule) => csstree.generate(rule))
        .join("\n");

      const browser = await puppeteer.launch({
        headless: "new",
        executablePath: "chromium",
        args: ["--no-sandbox", "--disable-gpu"],
      });

      const page = await browser.newPage();
      await page.goto(`http://localhost:3000?css=${btoa(fontFaceCss)}`, {
        waitUntil: "networkidle0",
      });

      await page.evaluate(() => {
        // @ts-ignore
        document.documentElement.style.height = "100%";
      });

      const horizontalOverflow = await page.evaluate(() => {
        // @ts-ignore
        const { scrollWidth, clientWidth } = document.documentElement;
        return scrollWidth > clientWidth;
      });

      const verticalOverflow = await page.evaluate(() => {
        // @ts-ignore
        const { scrollHeight, clientHeight } = document.documentElement;
        return scrollHeight > clientHeight;
      });

      const success = !(horizontalOverflow || verticalOverflow);

      await browser.close();

      return new Response(
        (
          <html lang="en">
            <head>
              <meta charset="UTF-8" />
              <title>Font Review</title>
              <link
                href="https://fonts.googleapis.com/css?family=Roboto+Mono"
                rel="stylesheet"
              />
              <link href="/styles.css" rel="stylesheet" />
            </head>
            <body>
              <div class="content">
                {success ? SuccessMessageComponent() : ErrorMessageComponent()}
              </div>
            </body>
          </html>
        ),
        {
          status: success ? 200 : 500,
          headers: { "Content-Type": "text/html" },
        }
      );
    },
    {
      body: t.Object({
        url: t.String(),
      }),
    }
  )
  .listen(3001);

const internalApp = new Elysia()
  .use(html())
  .get(
    "/style.js",
    () =>
      new Response(
        `document.querySelector("style").textContent = atob(new URLSearchParams(window.location.search).get("css"));`,
        {
          headers: {
            "Content-Type": "application/javascript",
          },
        }
      )
  )
  .get("/", async () => (
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Font Review</title>
        <style></style>
      </head>
      <body>
        <p style="font-family: content">{Bun.env.FLAG}</p>
        <script src="/style.js" />
      </body>
    </html>
  ))
  .listen(3000);

console.log(
  `🦊 Public Elysia app is running at ${app.server?.hostname}:${app.server?.port}`
);

console.log(
  `🦊 Internal Elysia app is running at ${internalApp.server?.hostname}:${internalApp.server?.port}`
);
