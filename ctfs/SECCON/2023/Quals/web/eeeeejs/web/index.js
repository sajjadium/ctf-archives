const express = require("express");
const { xss } = require("express-xss-sanitizer");
const { execFile } = require("node:child_process");
const util = require("node:util");

const app = express();
const PORT = 3000;

// Mitigation 1:
app.use(xss());

// Mitigation 2:
app.use((req, res, next) => {
  // A protection for RCE
  // FYI: https://github.com/mde/ejs/issues/735

  const evils = [
    "outputFunctionName",
    "escapeFunction",
    "localsName",
    "destructuredLocals",
    "escape",
  ];

  const data = JSON.stringify(req.query);
  if (evils.find((evil) => data.includes(evil))) {
    res.status(400).send("hacker?");
  } else {
    next();
  }
});

// Mitigation 3:
app.use((req, res, next) => {
  res.set("Content-Security-Policy", "default-src 'self'");
  next();
});

app.get("/", async (req, res) => {
  req.query.filename ??= "index.ejs";
  req.query.name ??= "ejs";

  const proc = await util
    .promisify(execFile)(
      "node",
      [
        // Mitigation 4:
        "--experimental-permission",
        `--allow-fs-read=${__dirname}/src`,

        "render.dist.js",
        JSON.stringify(req.query),
      ],
      {
        timeout: 2000,
        cwd: `${__dirname}/src`,
      }
    )
    .catch((e) => e);

  res.type("html").send(proc.killed ? "Timeout" : proc.stdout);
});

app.listen(PORT);
