const {promises: fs} = require('fs');
const fastify = require('fastify');

const flag = process.env.FLAG || 'DUMMY{DUMMY}';

const app = fastify();
app.get('/', async (_, res) => {
	res.type('text/html').send(await fs.readFile('index.html'));
});
app.post('/', (req, res) => {
	if (typeof req.body === 'object' && req.body[flag] === true) {
		return res.send(`Nice! flag is ${flag}`);
	}
	return res.send(`You failed...`);
});

app.listen(34705, '0.0.0.0');
