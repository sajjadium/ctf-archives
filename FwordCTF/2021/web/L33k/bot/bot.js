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
    	await page.goto('https://l33k.fword.tech/login',{
        waitUntil: 'networkidle2',  
        timeout:50000
    });

    // Login
    await page.type('#username', process.env.username);
    await page.type('#password', process.env.password);
    await page.click('#submit');
//    await page.waitForNavigation();

    // Get cookies
    const cookies = await page.cookies();
    // Use cookies in other tab or browser
    const page2 = await browser.newPage()
await page2.bringToFront();

    await page2.setCookie(...cookies);
    await page2.goto(website,{
        waitUntil: 'networkidle2',  
        timeout:50000
    }); // Opens page as logged user
	await delay(50000);
    	await browser.close();

}

app.get("/", (req,res)=>{
	var website=req.query.url ;
	visit(website).then((e)=>{res.send("Visited successfully!")});
//.catch((err)=>{res.send("Error")}) ;
})
app.listen(80,()=>{console.log("app listening")})
