import express from "express";
import rateLimit from "express-rate-limit";

import { visit, APP_URL } from "./bot.mjs";

const PORT = "1337";

const app = express();
app.use(express.json());

app.use(express.static("public"));

app.get("/app-url", async (req, res) => {
  return res.send(APP_URL);
});

app.use(
  "/api",
  rateLimit({
    // Limit each IP to 2 requests per 1 minute
    windowMs: 60 * 1000,
    max: 2,
  })
);

app.post("/api/report", async (req, res) => {
  const { url } = req.body;
  if (
    typeof url !== "string" ||
    (!url.startsWith("http://") && !url.startsWith("https://"))
  ) {
    return res.status(400).send("Invalid url");
  }

  try {
    await visit(url);
    return res.sendStatus(200);
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

app.listen(PORT);
