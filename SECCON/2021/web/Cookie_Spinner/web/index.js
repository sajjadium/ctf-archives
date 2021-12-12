const crypto = require("crypto");
const express = require("express");
const fs = require("fs");

const PORT = process.env.PORT || process.exit(1);

const app = express();
app.use(express.urlencoded());

app.use((req, res, next) => {
  const nonce = crypto.randomBytes(32).toString("base64");
  res.setHeader(
    "Content-Security-Policy",
    `default-src 'self'; script-src 'nonce-${nonce}'; base-uri 'none';`
  );
  req.nonce = nonce;
  next();
});

app.use("/static", express.static("static"));
app.use("/report", require("./report"));

const indexHtml = fs.readFileSync("index.html").toString();

const defaultView = `
  <div id="cookie" class="unclickable big spinner"></div>
`;

app.get("/", (req, res) => {
  // You can edit the cookie viewer!
  const view = req.query.view || defaultView;

  const html = indexHtml
    .replaceAll("{{NONCE}}", req.nonce)
    .replaceAll("{{VIEW}}", view);

  res.send(html);
});

app.listen(PORT, () => {
  console.log("Started");
});
