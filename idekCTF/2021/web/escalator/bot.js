const puppeteer = require("puppeteer");


const id = process.argv[3];

const browser_options = {
        headless: true,
        args: [
                '--no-sandbox',
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
                '--js-flags=--noexpose_wasm,--jitless'
        ],
        ignoreHTTPSErrors: true
};

const cookies = {
        name: "id",
        value: id,
        domain: "localhost:1337",
}
const clearURl = 'http://localhost:1337/admin'
async function visit_page(url) {
      
        const browser = await puppeteer.launch(browser_options);
        const page = await browser.newPage();
        await page.setCookie(cookies);
    
        try{
        await page.goto(url, {waitUntil: 'networkidle0', timeout: 200000});
        }catch (error){
                console.log('failed!');
                console.log(error);
                process.exit(1);
        }
       
        try{
            await page.goto(clearURl);
        }catch (error){
                console.log('failed!');
                console.log(error);
                process.exit(1);
        }
      
        await page.type('#entryForm', id);
        await page.keyboard.press('Enter');
        
        await browser.close();
        
        process.exit(0);
       
}


const url = process.argv[2];

visit_page(url).catch(()=>console.log('main program failed'));