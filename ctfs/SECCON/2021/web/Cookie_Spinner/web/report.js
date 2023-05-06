const net = require("net");
const express = require("express");

const BOT_HOST = process.env.BOT_HOST || process.exit(1);
const BOT_PORT = process.env.BOT_PORT || process.exit(1);

const router = express.Router();

const REPORT_DURATION = 30; // secs
const ipToLastTime = new Map(); // (ip: string) -> Time

router.post("/", (req, res) => {
  const url = req.body.url;
  if (url == null) {
    res.status(400).send("Url not found");
    return;
  }
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    res.status(400).send("Bad url :(");
    return;
  }

  const ip = req.ip;
  const time = Date.now();
  if (ipToLastTime.has(ip)) {
    const diff = (time - ipToLastTime.get(ip)) / 1000; // secs
    const rest = Math.floor(REPORT_DURATION - diff);
    if (rest > 0) {
      res.status(400).send(`Please wait ${rest} secs`);
      return;
    }
  }
  ipToLastTime.set(ip, time);

  try {
    const client = net.connect(BOT_PORT, BOT_HOST, () => {
      client.write(url);
    });

    let response;
    client.on("data", (data) => {
      response = data.toString();
      client.end();
    });

    client.on("end", () => res.send(response));
  } catch (e) {
    console.log(e);
    res.status(500).send("Something wrong...");
  }
});

module.exports = router;
