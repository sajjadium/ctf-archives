import OpenAI from 'openai';
import { createServer } from 'http';
import ejs from 'ejs';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const system = [
	'You are a web application firewall',
	'Your goal is to stop attempted hacking attempts',
	'I will give you a submission and you will respond with H or R, only a single letter',
	'H means hacking attempt, R means not a hacking attempt'
].join('. ')


const html = `<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>gpwaf</title>
	<style>
		* {
			font-family: monospace;
		}
		#content {
			margin-left: auto;
			margin-right: auto;
			width: 100%;
			max-width: 830px;
		}
		button {
			font-size: 1.5em;
		}
		textarea {
			width: 100%;
		}
	</style>
</head>
<body>
	<div id="content">
		<h1>gpwaf</h1>
		<p>i made a ejs renderer, its 100% hack proof im using gpt to check all your queries!</p>
		<form>
			<textarea name="template" placeholder="template" rows="30"><%= query %></textarea>
			<br>
			<button>run!</button>
		</form>
		<br>
		<pre><%= result %></pre>
	</div>
</body>
</html>`

async function check(template) {
	return (await openai.chat.completions.create({
		model: 'gpt-3.5-turbo-0125',
		messages: [{
			role: 'system',
			content: system
		}, {
			role: 'user',
			content: template
		}],
	})).choices[0].message.content
}

createServer(async (req, res) => {
	const template = new URL(req.url, 'http://localhost').searchParams.get('template');
	if (!template) {
		return res.end(ejs.render(html, {
			query: '',
			result: 'result goes here!'
		}));
	}

	if (/[^\x20-\x7F \r\n]/.test(template)) {
		return res.end(ejs.render(html, {
			query: template,
			result: 'printable ascii only!'
		}))
	}

	if (template.length > 500) {
		return res.end(ejs.render(html, {
			query: template,
			result: 'too long!'
		}))
	}

	const result = await check(template);
	if (result !== 'R') {
		return res.end(ejs.render(html, {
			query: template,
			result: 'hacking attempt!',
		}));
	}

	try {
		return res.end(ejs.render(html, {
			query: template,
			result: ejs.render(template),
		}));
	} catch(e) {
		return res.end(ejs.render(html, {
			query: template,
			result: e.toString()
		}));
	}
}).listen(8080);
