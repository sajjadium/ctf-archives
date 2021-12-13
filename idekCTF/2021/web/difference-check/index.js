const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const ssrfFilter = require('ssrf-req-filter');
const fetch = require('node-fetch');
const Diff = require('diff');
const hbs = require('express-handlebars');
const port = 1337;
const flag = 'idek{REDACTED}';


app.use(bodyParser.urlencoded({ extended: true }));
app.engine('hbs', hbs.engine({
    defaultLayout: 'main',
    extname: '.hbs'
}));

app.set('view engine', 'hbs');


async function validifyURL(url){
	valid = await fetch(url, {agent: ssrfFilter(url)})
	.then((response) => {
		return true
	})
	.catch(error => {
		return false
	});
	return valid;
};

async function diffURLs(urls){
	try{
		const pageOne = await fetch(urls[0]).then((r => {return r.text()}));
		const pageTwo = await fetch(urls[1]).then((r => {return r.text()}));
		return Diff.diffLines(pageOne, pageTwo)
	} catch {
		return 'error!'
	}
};

app.get('/', (req, res) => {
	res.render('index');
});

app.get('/flag', (req, res) => {
	if(req.connection.remoteAddress == '::1'){
		res.send(flag)}
	else{
		res.send("Forbidden", 503)}
});

app.post('/diff', async (req, res) => {
	let { url1, url2 } = req.body
	if(typeof url1 !== 'string' || typeof url2 !== 'string'){
		return res.send({error: 'Invalid format received'})
	};
	let urls = [url1, url2];
	for(url of urls){
		const valid = await validifyURL(url);
		if(!valid){
			return res.send({error: `Request to ${url} was denied`});
		};
	};
	const difference = await diffURLs(urls);
	res.render('diff', {
		lines: difference
	});

});

app.listen(port, () => {
	console.log(`App listening at http://localhost:${port}`)
});
