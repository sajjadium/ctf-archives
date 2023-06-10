const express = require('express')
const bot = require('./bot')

const public_domain = process.env["PUBLIC_DOMAIN"] || "bank.flagify3.fibonhack.it";
const internal_domain = process.env["INTERNAL_DOMAIN"] || "flagify3_frontend";

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/visit', async function (req, res) {
	try {
		let url = req.body.url;

		if(url && typeof url == "string" && url.startsWith(`http://${public_domain}/`)){
			url = url.replace(public_domain, internal_domain);
			console.log("Bot is visiting: ", url)
			bot.visit(url);
			res.send('Admin will visit the page soon');	
		}
		else{
			res.send('Invalid URL ://');
		}
	} catch (e) {
		console.log(e);
		res.status(400);
		res.send('bad url');
	}
})


app.listen(8080, '0.0.0.0');
