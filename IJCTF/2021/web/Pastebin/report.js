const puppeteer = require('puppeteer')

function delay(time) {
   return new Promise(function(resolve) {
       setTimeout(resolve, time)
   });
}

async function visit(url) {
        const browser = await puppeteer.launch({ args: ['--no-sandbox'] })
        var page = await browser.newPage();
        await page.setCookie({name: 'flag', value: process.env.FLAG, domain: 'localhost:1337'})
        await page.goto(url, { waitUntil: 'networkidle2' })
        await delay(3000);
        await page.close()
        await browser.close()
}

function report(req,res) {
  var url = req.body.url;
  visit(url).then((e)=>{res.send("Visted")})
}


module.exports = {report}
