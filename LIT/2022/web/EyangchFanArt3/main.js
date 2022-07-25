require("dotenv").config();

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const ejs = require("ejs");
const {component, parseXML, generateArt} = require("./canvasMaker.js");

app.use(bodyParser.urlencoded({ extended: true }));

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
	res.render("index");
});



app.post('/makeArt', (req, res) => {
	var code = req.body.code;
	const secretPassword = require("crypto").randomBytes(8).toString('hex');
	var flag = `
<component name="flag" password="` + secretPassword + `">
	<text color="black" font="bold 10pt Arial">` + (process.env.FLAG ?? "ctf{flag}") + `</text>
</component>

<flag x="100" y="400" password="` + secretPassword + `"></flag>
	`;

	var eyangComp = `
<component name="EYANGOTZ">
	<component name="eyes1">
		<line x1="10" y1="80" x2="30" y2="60" color="#1089f5" width="20"></line>
		<line x1="30" y1="60" x2="60" y2="70" color="#1089f5" width="20"></line>
	</component>
	<component name="eyes2">
		<line x1="110" y1="50" x2="130" y2="30" color="#1089f5" width="20"></line>
		<line x1="130" y1="30" x2="160" y2="40" color="#1089f5" width="20"></line>
	</component>
	<component name="mouth">
		<line x1="40" y1="200" x2="50" y2="220" color="#1089f5" width="20"></line>
		<line x1="50" y1="220" x2="190" y2="200" color="#1089f5" width="20"></line>
		<line x1="190" y1="200" x2="200" y2="180" color="#1089f5" width="20"></line>
	</component>
	<text x="30" y="30" font="bold 10pt Arial">EYANG SO OTZ</text>
</component>
<EYANGOTZ x="10" y="50"></EYANGOTZ>
<EYANGOTZ x="350" y="100"></EYANGOTZ>
<EYANGOTZ x="50" y="190"></EYANGOTZ>
<EYANGOTZ x="130" y="200"></EYANGOTZ>
<EYANGOTZ x="200" y="190"></EYANGOTZ>
<EYANGOTZ x="150" y="300"></EYANGOTZ>
	`

	code = "<fanart>" + flag + eyangComp + code + "</fanart>";

	generateArt(code,res);
});

app.listen(8080, () => {
	console.log("EYANG OTZ OTZ OTZ OTZ!!!");
});