import { Application, helpers } from 'https://deno.land/x/oak/mod.ts';

const HOST = '0.0.0.0';
const PORT = 8080;

let PROVIDER_TOKEN = Deno.env.get('PROVIDER_TOKEN');
const FLAG = await Deno.readTextFile('./flag.txt');

const app = new Application();

app.use((ctx) => {
  const params = helpers.getQuery(ctx);
  if (!params.token) return;

  const token = params.token;
  if (token === PROVIDER_TOKEN) {
    ctx.response.body = `export const FLAG = '${FLAG}';`;
  };
});

app.addEventListener('listen', ({ hostname, port }) => {
  console.log(`Listening on: ${hostname}:${port}`);
});

await app.listen({ hostname: HOST, port: PORT });
