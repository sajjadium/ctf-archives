var express = require('express');
const puppeteer = require('puppeteer');
var router = express.Router();

var port = Number.parseInt(process.env.PORT || '3000');

/* GET users listing. */
router.post('/', async function(req, res, next) {

  res.setHeader('transfer-encoding', 'chunked');
  res.setHeader('Content-Type', 'text/html; charset=UTF-8');

  res.write("Thanks for sending a report. An admin is looking into this now...\n<br>");

  const img = req.body.image;
  try {
    const browser = await puppeteer.launch({args: ['--no-sandbox', '--headless', '--disable-gpu']});
    const page = await browser.newPage();

    await page.setCookie({
      "name": "flag",
      "value": process.env.FLAG,
      "url": "http://localhost:" + port
    });

    await page.setRequestInterception(true);
    page.once('request', request => {
      var data = {
        "method": "POST",
        "postData": "image=" + encodeURIComponent(img),
        'headers': {
          ...request.headers(),
          'Content-Type': 'application/x-www-form-urlencoded'
        },
      };

      console.log(data);

      request.continue(data);

      page.setRequestInterception(false);

    });

    const resp = await page.goto('http://localhost:' + port + "/", {waitUntil: 'networkidle2'});
    await new Promise(resolve => setTimeout(resolve, 5000));
  
    await browser.close();

    res.write("An admin has seen your bug report. Thank you.");

    res.end();
  }catch(e) {
    res.write("An error has occurred. Please try again later.");
    res.end();
    console.log(e);
    return;
  }
});

module.exports = router;
