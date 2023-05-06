const assign = require("nested-object-assign");
const express = require("express");
const fs = require("fs");
const multer = require("multer");
const morgan = require("morgan");
const { spawn } = require("child_process");

// config
const UPLOAD_DIR = process.env.UPLOAD_DIR ?? "/tmp";
const ZIP_OPTS = JSON.parse(process.env.ZIP_OPTS ?? '{"executable":"zip"}');

// zipper
function zip(infile, outfile, extra_opts) {
  const opts = assign(
    {
      zip: {
        password: null,
        compressionMethod: "deflate",
      },
      executable: ZIP_OPTS.executable,
    },
    extra_opts
  );

  return spawn(ZIP_OPTS.executable, [
    "-j",
    outfile,
    infile,

    "--compression-method",
    opts.zip.compressionMethod,

    ...(opts.zip.password
      ? ["--encrypt", "--password", opts.zip.password]
      : []),

    ...(ZIP_OPTS.extra_opts ?? []),
  ]);
}

function tryRm(file) {
  try {
    fs.unlinkSync(file);
  } catch (e) {}
}

// app
const app = express();
app.use(morgan("tiny"));

const zipUpload = multer({
  dest: UPLOAD_DIR,
  limits: {
    files: 1,
    fileSize: 8192,
  },
}).single("file");

app.post("/zip", zipUpload, (req, res) => {
  if (!req.file) return res.redirect("/");
  const outfile = `${req.file.path}.zip`;

  function abort(status) {
    tryRm(req.file.path);
    tryRm(outfile);
    res.status(status).end();
  }

  zip(req.file.path, outfile, { zip: req.body })
  .on("error", () => abort(500))
  .on("exit", (code) => {
    if (code !== 0) return abort(500);

    fs.createReadStream(outfile)
      .on("error", () => abort(500))
      .on("finish", () => abort(200))
      .pipe(res)
  });
});

app.get("/", (_req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.listen(8000, () => {
  console.log("App started");
});
