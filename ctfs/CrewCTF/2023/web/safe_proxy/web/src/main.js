import { Application, Router, helpers } from 'https://deno.land/x/oak/mod.ts';
import { encode } from 'https://deno.land/std/encoding/hex.ts';

const HOST = '0.0.0.0';
const PORT = 8080;

const PROVIDER_TOKEN = Deno.env.get('PROVIDER_TOKEN');
const PROVIDER_HOST = Deno.env.get('PROVIDER_HOST');
const { FLAG } = await import(`http://${PROVIDER_HOST}/?token=${PROVIDER_TOKEN}`);
// no ssrf!
await Deno.permissions.revoke({ name: 'net', host: PROVIDER_HOST});


const router = new Router();

router
  .get('/', async (ctx) => {
    const encoded = new TextEncoder().encode(FLAG);
    const hash_buff = await crypto.subtle.digest('sha-256', encoded);
    const hash = new TextDecoder().decode(encode(new Uint8Array(hash_buff)));
    const html = await Deno.readTextFile('./index.html');
    ctx.response.body = html.replace('{HASH}', hash);
  })

  .get('/proxy', async (ctx) => {
    const params = helpers.getQuery(ctx);

    if (!params.url) {
      ctx.response.body = 'missing url';
      return;
    }

    const url = params.url;
    const fetchResponse = await fetch(url);
    ctx.response.body = fetchResponse.body;
  })
;

const app = new Application();

app.use(router.routes());
app.use(router.allowedMethods());

app.addEventListener('listen', ({ hostname, port }) => {
  console.log(`Listening on ${hostname}:${port}`);
});

await app.listen({ hostname: HOST, port: PORT });
