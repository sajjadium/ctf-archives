require("dotenv").config();

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const ejs = require("ejs");
var {component, parseXML, viewFanfic} = require("./fanficMaker.js");

app.use(bodyParser.urlencoded({ extended: true }));

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
	res.render("index");
});

app.post('/makeFanfic', (req, res) => {
	var code = req.body.code;
	const root1 = "a" + require("crypto").randomBytes(8).toString('hex');
	const root2 = "a" + require("crypto").randomBytes(8).toString('hex');

	code = "<" + root1 + ">" + code + "</" + root1 + ">";
	code += "<" + root2 + ">" + " <fanfic name='eyangORZ' prefix='OMG DID YOU KNOW THAT THE FLAG IS " + process.env.FLAG + "'></fanfic> <eyangORZ></eyangORZ>" + "</" + root2 + ">";

	viewFanfic("<root>" + code + "</root>",res,root1,root2);
});

app.listen(4242, () => {
	console.log("EYANG OTZ OTZ OTZ OTZ!!!");
});