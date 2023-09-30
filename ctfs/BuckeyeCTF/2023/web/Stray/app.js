import express from "express";
import path from "path";
import fs from "fs";

const app = express();

app.get("/cat", (req, res) => {
  let { category } = req.query;

  console.log(category);

  if (category.length == 1) {
    const filepath = path.resolve("./names/" + category);
    const lines = fs.readFileSync(filepath, "utf-8").split("\n");
    const name = lines[Math.floor(Math.random() * lines.length)];

    res.status(200);
    res.send({ name });
    return;
  }

  res.status(500);
  res.send({ error: "Unable to generate cat name" });
});

app.get("/", (_, res) => {
  res.status(200);
  res.sendFile(path.resolve("index.html"));
});

app.listen(process.env.PORT || 3000);
