const express = require("express");
const bodyParser = require("body-parser");
const morgan = require("morgan");
const flagcmp = require("./impl");

const flag = process.env["FLAG"];
if (!flag) {
  throw new Error("Expected FLAG to be present in env.");
}

const port = process.env["PORT"];
if (!port) {
  throw new Error("Port to listen on should be specified in env.");
}

flagcmp.set_flag(flag);

const app = express();
app.set("view engine", "pug");
app.set("views", __dirname + "/views");

app.use(bodyParser.urlencoded({ extended: false }));
app.use(morgan("short"));

app.get("/", (_, res) => {
  res.render("index");
});

app.post("/", (req, res) => {
  const guess = req.body.guess || "";
  const result = flagcmp.run(guess);
  res.render("index", { result });
});

app.listen(port, () => {
  console.log(`FlagCMP is serving port ${port}`);
});
