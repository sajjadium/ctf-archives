// Notepad 2 : Ken's Chronicle
const puppeteer = require('puppeteer');


const challName = "Notepad 2"

const thecookie = {
    name: 'id',
    value: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    domain: 'chall.notepad2.gq',
    expires: -1,
    httpOnly: true,
    secure: true,
    session: true,
    sameSite: 'None',
  }



async function url_visit (url) {
    var quote;
    return new Promise(async function(resolve, reject) {
        // start modification
        
        const browser = await puppeteer.launch({executablePath: '/home/bot/latest/chrome'});  // add `{ args: ['--no-sandbox'] }` if running as root
        const page = await browser.newPage();         
        await page.setCookie(thecookie)
        try{
            var result = await page.goto(url);
            await page.waitForTimeout(1e3*17);// wait for 17 seconds before closing              
        }
        catch(e){
            console.log("timeout exceeded");
        }        
        await browser.close();

        // end modification
        resolve(quote);
    });
}


function popMe(){
    queue.pop(queueName,sendUrl)
}

async function sendUrl(err, url) {
    if (err) {
        throw err;
    }

    if (!url) {
        setTimeout(popMe, 1e3*2); // if null is returned, wait for 2 secs before retrying
    } else {
        console.log(url)
        q = await url_visit(url)
        popMe();
    } 
}


url = "<your url>"
url_visit(url)