const express = require("express");
const sqlite3 = require("sqlite3");
const fs = require("fs");

const app = express();
const db = new sqlite3.Database(":memory:");

const flag = fs.readFileSync("./flag.txt", { encoding: "utf8" }).trim();
const crystals = require("./crystals");

db.serialize(() => {
  db.run("CREATE TABLE crystals (name TEXT, price REAL, quantity INTEGER)");

  const stmt = db.prepare("INSERT INTO crystals (name, price, quantity) VALUES (?, ?, ?)");

  for (const crystal of crystals) {
    stmt.run(crystal["name"], crystal["price"], crystal["quantity"]);
  }
  stmt.finalize();

  db.run("CREATE TABLE IF NOT EXISTS flag (flag TEXT)");
  db.run(`INSERT INTO flag (flag) VALUES ('${flag}')`);
});

app.get("/crystals", (req, res) => {
  const { name } = req.query;

  if (!name) {
    return res.status(400).send({ err: "Missing required fields" });
  }

  db.all(`SELECT * FROM crystals WHERE name LIKE '%${name}%'`, (err, rows) => {
    if (err) {
      console.error(err.message);
      return res.status(500).send('Internal server error');
    }

    return res.send(rows);
  });
});

app.get("/", (req, res) => {
  res.sendfile(__dirname + "/index.html");
});

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});

