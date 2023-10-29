import express from "express";
import { engine } from "express-handlebars";
import fileUpload from "express-fileupload";
import config from "./config";

import path from "path";
import {
  getAvailableChallenges,
  loadChallenge,
  sanitizeName,
} from "./challenges";
import { createAttempt, loadAttempt } from "./attempts";
import { helpers } from "./handlebars-helpers";
import { RipesVerifier } from "./ripesVerifier";

const app = express();

app.engine(
  "handlebars",
  engine({
    helpers: helpers,
  })
);
app.set("view engine", "handlebars");
app.set("views", "views");

app.use(
  fileUpload({
    limits: { fileSize: 20 * 1024, files: 1 },
    abortOnLimit: true,
    responseOnLimit: "You must only upload files with a size of up to 20kB.",
    createParentPath: true,
  })
);

app.get("/", (req, res) => {
  res.render("home");
});

app.get("/health", (req, res) => {
  res.sendStatus(200);
});

app.get("/favicon.ico", (req, res) => {
  res.sendStatus(404);
});

app.use("/css", express.static("node_modules/water.css/out/"));
app.use("/res", express.static("res/"));

app.get("/download/:challenge.s", async (req, res) => {
  try {
    const unsanitizedChallenge = req.params.challenge;
    const challengeName = sanitizeName(unsanitizedChallenge);

    if (!(await getAvailableChallenges()).includes(challengeName)) {
      return res.sendStatus(404);
    }

    const downloadPath = path.join(
      path.resolve("."),
      config.challengePath,
      challengeName,
      "template.s"
    );

    if (downloadPath === "/home/node/flag.txt") {
      return res.sendStatus(403);
    }

    res.sendFile(downloadPath);
  } catch (e) {
    return res.sendStatus(500);
  }
});

app.get("/result/:uuid", async (req, res) => {
  try {
    const attempt = await loadAttempt(req.params.uuid);
    const challenge = await loadChallenge(attempt.challenge);
    res.render("result", { attempt, challenge });
  } catch (e) {
    return res.sendStatus(500);
  }
});

app.post("/upload", async function (req, res) {
  try {
    if (!req.files || Object.keys(req.files).length === 0) {
      return res.status(400).send("No files were uploaded.");
    }

    const uploadFile = req.files.uploadFile;

    const challenge = req.body.challenge;

    if (Array.isArray(uploadFile)) {
      return res
        .status(400)
        .send("It seems like multiple files were uploaded.");
    }

    const attempt = await createAttempt(uploadFile, challenge);
    const verifier = new RipesVerifier();
    verifier.runAttempt(attempt.uuid);
    res.redirect(`/result/${attempt.uuid}`);
  } catch (e) {
    console.error(e);
    return res.sendStatus(500);
  }
});

app.get("/:challenge", async (req, res) => {
  try {
    const unsanitizedChallenge = req.params.challenge;
    const challengeName = sanitizeName(unsanitizedChallenge);

    if (!(await getAvailableChallenges()).includes(challengeName)) {
      return res.sendStatus(404);
    }

    const challenge = await loadChallenge(challengeName);
    res.render("challenge", {
      challenge,
    });
  } catch (e) {
    console.error(e);
    return res.sendStatus(500);
  }
});

app.listen(config.port, () => {
  console.log(`Server started on port ${config.port}`);
});
