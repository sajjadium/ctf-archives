const express=require('express');
const fetch= require('node-fetch');
const url = require('url');
const app=express();


const appUrl="seoftw";
const renderUrl = "http://rendertron:3000/render" ;

function generateUrl(request){
	return url.format({
		protocol: request.protocol,
		host: appUrl,
		pathname: request.originalUrl
	});
}

function detectBot(userAgent){
	const bots=[
		"googlebot",
		"bingbot",
		"twitterbot",
		"facebookexternalhit",
		"linkedinbot",
		"slackbot"
	]
	const agent = userAgent.toLowerCase();
	for (const bot of bots){
		if (agent.indexOf(bot) > -1){
			return true;
		}
	}
	return false;
}



app.get("*", (req,res)=>{
	const isBot = detectBot(req.headers["user-agent"]);
	if (isBot){
		
		const botUrl = generateUrl(req);
		fetch(`${renderUrl}/${botUrl}`).then(res=>res.text())
		.then(body=> {
		res.set("Cache-Control","no-cache, no-store, must-revalidate");
		res.set("Pragma","no-cache");
		res.set("Expires","0");
		res.send(body.toString());
		
		});

	}
	else{
		fetch(generateUrl(req)).then(res=>res.text())
		.then(body=>{
			res.send(body.toString());
		});

	}

});

app.listen(3000,()=>{
	console.log("listening in 3000");
});
