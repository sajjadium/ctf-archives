const express = require("express");
const bodyParser = require('body-parser');
const fetch = require("node-fetch");
const puppeteer = require('puppeteer');

const app = express();
const captcha_secret_key = process.env.CAPTCHA_SECRET_KEY || "";
const flag = process.env.flag || "flag{test-flag}"
const challengeUrl = process.env.url || "http://localhost:4000/";
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

const isUrlValid = function(url){
	try{
		url = new URL(url);
	} catch(e){
		return false;
	}

	if(url.protocol != "http:" && url.protocol != "https:") return false;
	return true;
}

const crawl = async function(url){
 	const browser = await puppeteer.launch({pipe:true});

 	try{
 		const page = await browser.newPage();
	 	await page.goto(challengeUrl,{
      		timeout: 1000
    	});
		await page.setCookie({"name":"flag","value":flag,"sameSite":"Strict","httpOnly":false,"secure":false});
		await page.goto("about:blank",{
      		timeout: 1000
    	});
		await page.goto(url,{
      		timeout: 1000
    	});
    	await wait(3000);
	} catch(e){

	}
 	
	await browser.close();
}

app.use(express.static('static'));
app.use(bodyParser.urlencoded({
	extended : true
}));

app.get("/report",(req,res)=>{
	return res.sendFile(__dirname + "/static/report.html");
});

app.post("/report",(req,res)=>{
	var token = req.body["g-recaptcha-response"];
	var url = req.body["url"];

	if(!token || !url || !String(token).match(/^[0-9a-zA-Z_-]+$/) ){
		return res.send("No captcha");
	}
    token = String(token);

    fetch(`https://www.google.com/recaptcha/api/siteverify?secret=${captcha_secret_key}&response=${token}`, {
        method: 'post'
    })
    .then(response => response.json())
    .then(r => {
    	if(r.success == true){
    		url = String(url);
    		if(isUrlValid(url)){
    			crawl(url);
	    		res.send("OK");
    		} else {
	    		res.send("Url is not valid!");
    		}
    	} else {
			res.send("No");
    	}
    })
    .catch(error => res.send("No"));
})

app.listen(4000,()=>{
	console.log("Listening...");
})