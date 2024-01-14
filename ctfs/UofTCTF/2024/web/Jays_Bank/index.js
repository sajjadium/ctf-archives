const express = require("express");
const router = require("./routes");
const db = require("./utils/db.js");
const cookieParser = require("cookie-parser");
const app = express();

const Database = new db();

app.use(express.json());
app.use(cookieParser());
app.use(express.static("static"));
app.set("view engine", "ejs");

app.use("/", router(Database));

app.all("*", (req, res) => {
  res.status(404).send("404 Not Found");
});

app.listen(3000, () => {
  console.log("Listening on port 3000");
});
