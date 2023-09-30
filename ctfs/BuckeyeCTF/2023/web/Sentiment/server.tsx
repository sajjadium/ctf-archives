import { Elysia, t } from "elysia";
import { html } from "@elysiajs/html";
import { cookie } from "@elysiajs/cookie";
import { CustomElementHandler } from "typed-html";
import { marked } from "marked";
import puppeteer from "puppeteer";
import * as elements from "typed-html";

const NotebookIcon: CustomElementHandler = (attributes, contents) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 48 48"><g fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="4"><path d="M10 6a2 2 0 0 1 2-2h28a2 2 0 0 1 2 2v36a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2V6Z"/><path stroke-linecap="round" d="M34 6v36M6 14h8M6 24h8M6 34h8M27 4h12M27 44h12"/></g></svg>`;
const PencilIcon: CustomElementHandler = (attributes, contents) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none"><path d="M24 0v24H0V0h24ZM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035c-.01-.004-.019-.001-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.017-.018Zm.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022Zm-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01l-.184-.092Z"/><path fill="currentColor" d="M16.035 3.015a3 3 0 0 1 4.099-.135l.144.135l.707.707a3 3 0 0 1 .135 4.098l-.135.144L9.773 19.177a1.5 1.5 0 0 1-.562.354l-.162.047l-4.454 1.028a1.001 1.001 0 0 1-1.22-1.088l.02-.113l1.027-4.455a1.5 1.5 0 0 1 .29-.598l.111-.125L16.035 3.015Zm-.707 3.535l-8.99 8.99l-.636 2.758l2.758-.637l8.99-8.99l-2.122-2.12Zm3.536-2.121a1 1 0 0 0-1.32-.083l-.094.083l-.708.707l2.122 2.121l.707-.707a1 1 0 0 0 .083-1.32l-.083-.094l-.707-.707Z"/></g></svg>`;
const ReportIcon: CustomElementHandler = (attributes, contents) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><path fill="currentColor" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0a1 1 0 0 1 2 0Z"/></svg>`;

const Header: CustomElementHandler = (attributes, contents) => (
  <div class="header">
    <div class="container">
      <nav class="nav">
        <a
          class={`nav-item ${
            attributes.selected === "note" ? "nav-item-selected" : ""
          }`}
          href="/"
        >
          <div class="nav-item-inner">
            <NotebookIcon />
            <span>My Note</span>
          </div>
        </a>
        <a
          class={`nav-item ${
            attributes.selected === "edit" ? "nav-item-selected" : ""
          }`}
          href="/edit"
        >
          <div class="nav-item-inner">
            <PencilIcon />
            <span>Modfiy Note</span>
          </div>
        </a>
        <a
          class={`nav-item ${
            attributes.selected === "report" ? "nav-item-selected" : ""
          }`}
          href="/report"
        >
          <div class="nav-item-inner">
            <ReportIcon />
            <span>Report</span>
          </div>
        </a>
      </nav>
    </div>
  </div>
);

const defaultNoteContent = await Bun.file("default.md").text();

function escapeHTML(html: string): string {
  const escapeMap: { [key: string]: string } = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };

  return html.replace(/[&<>"']/g, (match) => escapeMap[match]);
}

const editScript = `
document.getElementById("update-note").addEventListener("click", function() {
  fetch("/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: document.getElementById("note").innerText }),
  });
});
`;

const app = new Elysia()
  .use(html())
  .use(
    cookie({
      httpOnly: true,
      secret: Bun.env.COOKIE_SECRET,
    })
  )
  .get("/styles.css", () => Bun.file("styles.css"))
  .get("/", ({ set, cookie: { note }, unsignCookie, setCookie }) => {
    set.headers["Content-Security-Policy"] = "connect-src 'none'";
    set.headers["X-Frame-Options"] = "DENY";

    let noteContent: string = defaultNoteContent;

    if (!note) {
      setCookie("note", defaultNoteContent, { signed: true });
    } else {
      const { valid, value } = unsignCookie(note);

      if (!valid) {
        set.status = 401;
        return "Unauthorized";
      }

      noteContent = value;
    }

    return (
      <BaseHtml title="Sentiment - Note">
        <body>
          <Header selected="note" />
          <div class="content">
            <div class="container">{marked.parse(noteContent)}</div>
          </div>
        </body>
      </BaseHtml>
    );
  })
  .get("/edit", ({ set, cookie: { note }, unsignCookie, setCookie }) => {
    set.headers["Content-Security-Policy"] = "connect-src 'self'";
    set.headers["X-Frame-Options"] = "DENY";

    let noteContent: string = defaultNoteContent;

    if (!note) {
      setCookie("note", defaultNoteContent, { signed: true });
    } else {
      const { valid, value } = unsignCookie(note);

      if (!valid) {
        set.status = 401;
        return "Unauthorized";
      }

      noteContent = value;
    }

    return (
      <BaseHtml title="Sentiment - Edit">
        <body>
          <Header selected="edit" />
          <div class="content">
            <div class="container">
              <button id="update-note">Update Note</button>
              <pre id="note" contenteditable="true">
                {escapeHTML(noteContent)}
              </pre>
            </div>
          </div>
          <script>{editScript}</script>
        </body>
      </BaseHtml>
    );
  })
  .post(
    "/edit",
    ({ body, setCookie }) => {
      setCookie("note", body.content, { signed: true });
    },
    {
      body: t.Object({
        content: t.String(),
      }),
    }
  )
  .get("/report", ({ set }) => {
    set.headers["Content-Security-Policy"] = "connect-src 'none'";
    set.headers["X-Frame-Options"] = "DENY";

    return (
      <BaseHtml title="Sentiment - Report">
        <body>
          <Header selected="report" />
          <div class="content">
            <div class="container">
              <h2>Report a bug</h2>
              <p>
                Let us know where on our website you are experiencing issues and
                an admin will review it right away.
              </p>
              <form method="POST">
                <input name="url" placeholder="URL to report..." />
                <button type="submit" id="report">
                  Report
                </button>
              </form>
            </div>
          </div>
        </body>
      </BaseHtml>
    );
  })
  .post(
    "/report",
    async ({ body, set }) => {
      const url = new URL(body.url);
      if (url.protocol !== "https:" && url.protocol !== "http:")
        return new Response("Invalid url", { status: 500 });

      const browser = await puppeteer.launch({
        headless: "new",
        executablePath: "chromium",
        args: ["--no-sandbox", "--disable-gpu"],
      });

      const page = await browser.newPage();
      await page.setCookie({
        name: "note",
        value: Bun.env.FLAG_COOKIE_VALUE!,
        domain: Bun.env.FLAG_COOKIE_DOMAIN,
        sameSite: "Lax",
        httpOnly: true,
        secure: true,
      });
      await page.goto(body.url, { waitUntil: "load", timeout: 15 * 1000 });
      await browser.close();
      set.redirect = "/report";
    },
    {
      body: t.Object({
        url: t.String(),
      }),
    }
  )
  .listen(3001);

const BaseHtml: CustomElementHandler = (attributes, contents) => `
  <!DOCTYPE html>
  <html lang="en">
  
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${attributes.title}</title>
    <link href="https://fonts.googleapis.com/css?family=Inter" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Roboto+Mono" rel="stylesheet">
    <link href="/styles.css" rel="stylesheet">
  </head>
  
  ${attributes.children}
  `;

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
