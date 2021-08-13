// Notepad1 - Snakehole's secret
const puppeteer = require('puppeteer');

const challName = "Notepad 1"

const thecookie = {
    name: 'id',
    value: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    domain: 'chall.notepad1.gq',  
    expires: -1,
    httpOnly: true,
    secure: false,
    session: true,
    sameSite: 'Lax',
  }



  async function url_visit (url) {
    var quote;
    return new Promise(async function(resolve, reject) {
        // start modification
        
        const browser = await puppeteer.launch({executablePath: 'chrome'});  // add `{ args: ['--no-sandbox'] }` if running as root
        const page = await browser.newPage();         
        await page.setCookie(thecookie)
        try{
            var result = await page.goto(url);
            await page.waitForTimeout(1e3*10);// wait for 10 seconds before closing              
        }
        catch(e){
            console.log("timeout exceeded");
        }        
        await browser.close();

        // end modification
        resolve(quote);
    });
}


url_visit(url)
