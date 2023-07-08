const express = require('express');
const bodyParser = require('body-parser');
const { visit } = require('./bot.js');

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));

const PORT = 8080;

const REPORT_DURATION = parseInt(process.env.REPORT_DURATION) || 60;
const ipToLastTime = new Map();

app.get('/', async (req, res) => {
  res.sendFile('./index.html', { root: __dirname });
})

app.post('/report', async (req, res) => {
  const ip = req.ip;
  const time = Date.now();
  if (ipToLastTime.has(ip)) {
    const diff = (time - ipToLastTime.get(ip)) / 1000;
    const rest = Math.floor(REPORT_DURATION - diff);
    if (rest > 0) {
      return res.status(400).send(`Please wait ${rest} secs`);
    }
  }
  ipToLastTime.set(ip, time);

  const v = req.body.v;
  try {
    await visit(v);
  } catch (e) {
    console.log(e);
    return res.status(500).send('Something wrong');
  }
  return res.status(200).send('Done');
})

app.listen(PORT, () => {
  console.log(`bot server listening on port ${PORT}`);
})
