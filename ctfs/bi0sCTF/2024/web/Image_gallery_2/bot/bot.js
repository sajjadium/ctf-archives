const puppeteer = require('puppeteer')
const FLAG = process.env.FLAG
const APP_HOST = process.env.APP_HOST

module.exports.visit = async function visit(url){


	if(!url.startsWith(APP_HOST+'/')){
		return;
	}

	try{
		browser = await puppeteer.launch({
		    pipe: true,
		    args: [
		        "--no-sandbox",
		        "--disable-setuid-sandbox",
		        "--js-flags=--noexpose_wasm,--jitless",
		        "--ignore-certificate-errors",
		        `--unsafely-treat-insecure-origin-as-secure=${APP_HOST}`
		    ],
		    executablePath: "/usr/bin/google-chrome-stable",
		    headless: 'new'
		});
		console.log("lauched br")

		let page = await browser.newPage();
		await page.goto(APP_HOST,{ waitUntil: 'domcontentloaded'});
		console.log("first visit")
        await page.evaluate((flag)=>{
            const fileInput = document.querySelector('input[type="file"]');

			const myFile = new File([flag], 'flag.png', {
				type: 'image/png',
				lastModified: new Date(),
			});

			const dataTransfer = new DataTransfer();
			dataTransfer.items.add(myFile);
			fileInput.files = dataTransfer.files;
			document.forms[0].submit()
					
        },FLAG)
		await page.waitForNavigation({ waitUntil: 'load' })
		console.log("after file upload")
		await page.close()
		page = await browser.newPage();
		await page.goto(url,{'waitUntil':'networkidle0', timeout:60000})
		await new Promise(r=>setTimeout(r,60000));


	}catch(e){ 
		console.log(e) 
		return "failed"
	}
	try{
		await browser.close();
		return "sucess"
	}catch(e){
		return "error"
	}
	
}
