const express = require("express");
const app = express();
const expressWS = require("express-ws")(app);
const PORT = 8080;

const questions = require("./questions.json")

app.ws("/ws", function(ws, req) {
  let count = 0;
  ws.on("message", (msg) => {
    if (count < 4 && questions[count]["answer"].includes(msg)) {
      ++count;
      ws.send(JSON.stringify(questions[count]));
    } else {
      count = 0;
      ws.send(JSON.stringify(questions[count]));
    }
  })
});

app.get("/", function(req, res) {
  res.sendFile("index.html", {root: __dirname})
});
app.get("/main.js", function(req, res) {
  res.sendFile("main.js", {root: __dirname})
});

app.listen(PORT, () => { console.log(PORT) })