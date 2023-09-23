const puppeteer = require('puppeteer')
const flag = process.env.FLAG || 'ASIS{test-flag}';

async function visit(url){
	let browser;

	if(!/^https?:\/\//.test(url)){
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
		        `--unsafely-treat-insecure-origin-as-secure=http://localhost:8000`
		    ],
		    executablePath: "/usr/bin/google-chrome-stable",
		    headless: 'new'
		});

		let page = await browser.newPage();

		await page.goto('http://localhost:8000/',{ timeout:3000 });
		await new Promise(r=>setTimeout(r,500))
		await page.evaluate((flag)=>{
			document.getElementById('secret-holder').value = flag;
			submitSecret();
		},flag);
		await new Promise(r=>setTimeout(r,500))
		await page.close();

		page = await browser.newPage();
		page.on('popup',async function (popup){
			try{
				/*
				Challenge author's note:
				The following loop is because sometimes puppeteer
				doesn't actually click.
				*/
				await popup.waitForSelector('#btn',{
					timeout: 3000
				});
				for(let i=0;i<30;i++){
					await popup.click('#btn');	
				}
			}catch(e){}
		});
		await page.goto(url,{ waitUntil: 'load', timeout:2000 });
		await new Promise(r=>setTimeout(r,10000));
	}catch(e){ console.log(e) }
	try{await browser.close();}catch(e){}
	process.exit(0)
}

visit(JSON.parse(process.argv[2]))
