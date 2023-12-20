import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import { MongoClient, ObjectId } from "mongodb";
import { bot, urlRegex } from "./utils/bot.js";
import { rateLimit } from "express-rate-limit";
import { duplicate } from "./utils/secure.js";

const isTest = process.env.VITEST;
const limiter = rateLimit({
  windowMs: process.env.TIMEOUT * 60 * 1000,
  limit: process.env.LIMIT,
  standardHeaders: "draft-7",
  legacyHeaders: false,
});
const uri = `${process.env.MONGO_URL}`;
const client = new MongoClient(uri);
let diaryCollection;

await client.connect();
const db = client.db("db");
diaryCollection = db.collection("entries");
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export async function createServer(
  root = process.cwd(),
  hmrPort,
  customLogger
) {
  const resolve = (p) => path.resolve(__dirname, p);

  const app = express();
  app.use(limiter);

  /**
   * @type {import('vite').ViteDevServer}
   */
  const vite = await (
    await import("vite")
  ).createServer({
    root,
    logLevel: isTest ? "error" : "info",
    server: {
      middlewareMode: true,
      watch: {
        usePolling: true,
        interval: 100,
      },
      hmr: {
        port: hmrPort,
      },
    },
    appType: "custom",
    customLogger,
  });

  app.use(vite.middlewares);
  app.use(express.json());

  app.get("/", async (req, res, next) => {
    try {
      const url = req.originalUrl;

      let template;
      template = fs.readFileSync(resolve("views/index.html"), "utf-8");
      template = await vite.transformIndexHtml(url, template);
      const render = (await vite.ssrLoadModule("/utils/router.js")).render;

      const appHtml = await render(url, __dirname, req);

      const html = template.replace(`<!--app-html-->`, appHtml);

      res.status(200).set({ "Content-Type": "text/html" }).end(html);
    } catch (e) {
      res.status(500).end(e.stack);
    }
  });
  app.post("/create", async (req, res, next) => {
    let obj = duplicate(req.body);

    if (obj.uname === "admin" && obj.pass == process.env.PASSWORD) {
      obj.isAdmin = true;
    }
    if (obj.isAdmin) {
      const newEntry = req.body;

      try {
        const result = await diaryCollection.insertOne(newEntry);
        return res.json({ code: result.insertedId });
      } catch (err) {
        console.error("Failed to insert entry", err);
        return res.status(500).json({ code: "err" });
      }
    }
    return res.json({ code: "err" });
  });
  app.post("/save", async (req, res, next) => {
    let { id, message } = req.body;

    try {
      await diaryCollection.updateOne(
        { _id: new ObjectId(id) },
        { $set: { message: message } }
      );
      return res.json({ code: "success" });
    } catch (err) {
      console.error("Failed to update diary entry", err);
      return res.status(500).json({ code: "err" });
    }
  });
  app.get("/report", async (req, res, next) => {
    try {
      const url = req.originalUrl;

      let template;
      template = fs.readFileSync(resolve("views/report.html"), "utf-8");
      template = await vite.transformIndexHtml(url, template);
      const render = (await vite.ssrLoadModule("/utils/router.js")).render;

      const appHtml = await render(url, __dirname, req);

      const html = template.replace(`<!--app-html-->`, appHtml);

      res.status(200).set({ "Content-Type": "text/html" }).end(html);
    } catch (e) {
      res.status(500).end(e.stack);
    }
  });

  app.post("/report", async (req, res, next) => {
    const { url } = req.body;
    if (!url) {
      return res.status(400).send({ msg: "Url is missing." });
    }
    if (!RegExp(urlRegex).test(url)) {
      return res
        .status(422)
        .send({ msg: "URL din't match this regex format " + bot.urlRegex });
    }
    if (await bot(url)) {
      return res.send({ msg: "Admin successfully visited the URL." });
    } else {
      return res.status(500).send({ msg: "Admin failed to visit the URL." });
    }
  });

  app.get("/posts/:id", async (req, res, next) => {
    try {
      const post = await diaryCollection.findOne({
        _id: new ObjectId(req.params.id),
      });
      if (!post) {
        return res.status(404).json({ code: "err" });
      }
      const url = req.originalUrl;

      let template;
      template = fs.readFileSync(resolve("views/post.html"), "utf-8");
      template = await vite.transformIndexHtml(url, template);
      const render = (await vite.ssrLoadModule("/utils/router.js")).render;

      const appHtml = await render(url, __dirname, req);

      const html = template.replace(`<!--app-html-->`, appHtml);

      res.status(200).set({ "Content-Type": "text/html" }).end(html);
    } catch (e) {
      res.status(500).end(e.stack);
    }
  });
  app.get("*", async (req, res) => {
    return res.status(404).json({ code: "err" });
  });
  return { app, vite };
}

createServer().then(({ app }) =>
  app.listen(3000, () => {
    console.log(process.env.APPURL);
  })
);
