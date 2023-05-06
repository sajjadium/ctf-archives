const puppeteer = require('puppeteer');


(async () => {
  const browser = await puppeteer.launch(
    {
      args: [
        '--no-sandbox',
      ]
    }
  );
  const page = await browser.newPage();

  var url = process.argv[2];
  var uAgent = process.argv[3];
  var base_url = process.env.BASE_URL;

  page.setExtraHTTPHeaders({
     'user-agent': uAgent,
  })

  const cookies = [{
    'name': 'auth',
    'value': '<REDACTED>',
    'domain': base_url,
    'httpOnly': true
  }];
  
  await page.setCookie(...cookies);

  console.log("Visiting: " + url)
  await page.goto(url);
  await page.waitFor(10000)
  

  await browser.close();
})().catch((error)=>{
  console.log(error);
});
