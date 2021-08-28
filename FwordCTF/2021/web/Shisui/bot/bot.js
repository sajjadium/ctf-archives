const puppeteer = require('puppeteer');
const express= require("express");
const app=express();

const browser_options = {
    headless: true,
    args: [
        '--no-sandbox',
        '--disable-background-networking',
        '--disable-default-apps',
        '--disable-extensions',
        '--disable-gpu',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
    ],
};
function delay(timeout) {
  return new Promise((resolve) => {
    setTimeout(resolve, timeout);
  });
}

async function visit(website){
	const browser = await puppeteer.launch(browser_options);
        const page = await browser.newPage();
        await page.goto(website, {
        waitUntil: 'load',
        timeout:0

    });
        await delay(30000);
        await browser.close();
}

app.get("/", (req,res)=>{
	var website=req.query.url ;
	visit(website).then((e)=>{res.send("Visited successfully!")}).catch((err)=>{res.send("Error")}) ;
})
app.listen(80,()=>{console.log("app listening")})
