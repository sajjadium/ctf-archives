const express = require('express');
const path = require('path');
const cron = require("node-cron");
const bodyParser = require("body-parser");
const fs = require('fs');

const port = 3000;
const REPORTING_ENDPOINT_BASE = "https://53ea470eda222548025a34ec17f08b3a.report-uri.com";
const FLAG = process.env.FLAG;

const app = express();
app.use('/', express.static(__dirname + '/'));
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.use(function(req, res, next) {
	try{
		reportAPI = `{"group":"public","max_age":${60*60*60},"endpoints":[{"url":"${REPORTING_ENDPOINT_BASE}/?path=${req.originalUrl}"}],"include_subdomains":true}`;
		res.set("Report-To", reportAPI );
		res.set('Access-Control-Allow-Origin', ['*']);
		res.set("Content-Security-Policy", "default-src 'self'; img-src 'self'; font-src fonts.gstatic.com 'self'; style-src * 'self' 'unsafe-inline'; object-src 'self'; report-to "+JSON.parse(decodeURI(reportAPI)).group );
		res.set('Access-Control-Allow-Methods', 'GET,POST');
		res.set('X-Reports-Count', reportsCounter());
		next();
	}catch(e){
		res.status(500).send("Something Broke!");
	}
})

app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname+'/index.html'));
})

app.get('/report', (req, res) => {
	res.sendFile(path.join(__dirname+'/report.html'));
})

app.get('/vdp', (req, res) => {
	res.sendFile(path.join(__dirname+'/vdp.html'));
})

app.post('/report', (req, res) => {
	var vulnURL = req.body.url;
	if (!isValidHttpUrl(vulnURL)) {
		res.status(400).json({ message: "Vulnerable URL should starts with http:// or https:// ." })
	}else{
		let fullReport = {
	  	researcherName : req.body.name,
	  	researcherEmail: req.body.email,
	  	vulnURL: vulnURL,
	  	description: req.body.description
  	}
  	submitReport(fullReport);
  	res.status(200).json({ message: "Report submitted successfully!" })
	}
})

app.get('/flag', (req, res) => {
	if(req.socket.remoteAddress === "::ffff:127.0.0.1"){
		res.send(FLAG) 
	}else{
		res.send("Can be accessed internally only!")
	}
})

function isValidHttpUrl(string) {
  try {
    const url = new URL(string);
    return url.protocol === 'http:' || url.protocol === 'https:';
  } catch (err) {
    return false;
  }
}

function submitReport(fullReport){
	// REDACTED
}

function reportsCounter(){
	// REDACTED
}

app.listen(port, () => {
  console.log(`Server listening on Port ${port}`)
})