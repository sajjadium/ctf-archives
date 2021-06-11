const visiter = require('./visiter');

const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');

const app = express();

app.use(bodyParser.json());
app.use(cookieParser());

app.use(express.static('public'));

const nothisisntthechallenge = crypto.randomBytes(64).toString('hex');
const shares = new Map();
shares['hint'] = {name: '<marquee>helvetica standard</marquee>', score: 42};

app.post('/record', function (req, res) {
	if (req.body.name > 100) {
		return res.status(400).send('your name is too long! we don\'t have that kind of vc investment yet...');
	}

	if (isNaN(req.body.score) || !req.body.score || req.body.score < 1) {
		res.send('your score has to be a number bigger than 1! no getting past me >:(');
		return res.status(400).send('your score has to be a number bigger than 1! no getting past me >:(');
	}

	const name = req.body.name;
	const score = req.body.score;
	const shareName = crypto.randomBytes(8).toString('hex');

	shares[shareName] = { name, score };

	return res.redirect(`/shares/${shareName}`);
})

app.get('/shares/:shareName', function(req, res) {
	// TODO: better page maybe...? would attract those sweet sweet vcbucks
	if (!(req.params.shareName in shares)) {
		return res.status(400).send('hey that share doesn\'t exist... are you a time traveller :O');
	}

	const share = shares[req.params.shareName];
	const score = share.score;
	const name = share.name;
	const nonce = crypto.randomBytes(16).toString('hex');
	let extra = '';

	if (req.cookies.no_this_is_not_the_challenge_go_away === nothisisntthechallenge) {
		extra = `deletion token: <code>${process.env.FLAG}</code>`
	}

	return res.send(`
<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv='Content-Security-Policy' content="script-src 'nonce-${nonce}'">
		<title>snek nomnomnom</title>
	</head>
	<body>
		${extra}${extra ? '<br /><br />' : ''}
		<h2>snek goes <em>nomnomnom</em></h2><br />
		Check out this score of ${score}! <br />
		<a href='/'>Play!</a> <button id='reporter'>Report.</button> <br />
		<br />
		This score was set by ${name}
		<script nonce='${nonce}'>
function report() {
	fetch('/report/${req.params.shareName}', {
		method: 'POST'
	});
}

document.getElementById('reporter').onclick = () => { report() };
		</script> 
		
	</body>
</html>`);
});

app.post('/report/:shareName', async function(req, res) {
	if (!(req.params.shareName in shares)) {
		return res.status(400).send('hey that share doesn\'t exist... are you a time traveller :O');
	}

	await visiter.visit(
		nothisisntthechallenge,
		`http://localhost:9999/shares/${req.params.shareName}`
	);
})

app.listen(9999, '0.0.0.0');
