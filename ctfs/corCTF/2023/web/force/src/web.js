import fastify from 'fastify'
import mercurius from 'mercurius'
import { randomInt } from 'crypto'
import { readFile } from 'fs/promises'

const app = fastify({
    logger: true
});
const index = await readFile('./index.html', 'utf-8');

const secret = randomInt(0, 10 ** 5); // 1 in a 100k??

let requests = 10;

setInterval(() => requests = 10, 60000);

await app.register(mercurius, {
    schema: `type Query {
        flag(pin: Int): String
    }`,
    resolvers: {
        Query: {
            flag: (_, { pin }) => {
                if (pin != secret) {
                    return 'Wrong!';
                }
                return process.env.FLAG || 'corctf{test}';
            }
        }
    },
    routes: false
});

app.get('/', (req, res) => {
    return res.header('Content-Type', 'text/html').send(index);
});

app.post('/', async (req, res) => {
    if (requests <= 0) {
        return res.send('no u')
    }
    requests --;
    return res.graphql(req.body);
});

app.listen({ host: '0.0.0.0', port: 80 });