import { Application, Router } from "https://deno.land/x/oak@v11.1.0/mod.ts";
import apiRouter from './api.js';


// Load .env
const conf = Deno.env.toObject();
if (!conf.PASSWORD || !conf.SESSION_KEY) {
    console.log('.env missing')
    conf.PASSWORD = 'admin';
    conf.SESSION_KEY = 'secret';
}

// Init with cookie signing key
const app = new Application({keys: [conf.SESSION_KEY]});
const router = new Router();


router.get('/', async (ctx) => {
   await ctx.send({root: `${Deno.cwd()}/static`, path: 'index.html'});
});


router.get('/login', async (ctx) => {
    await ctx.send({root: `${Deno.cwd()}/static`, path: 'login.html'});
});

router.post('/login', async (ctx) => {
    const body = ctx.request.body({ type: 'form' })
    const value = await body.value
    if (value.get('username') === 'admin' && value.get('password') === conf.PASSWORD) {
        await ctx.cookies.set('admin', '1', {
            httpOnly: true, 
            secure: true , 
            sameSite: 'none', 
            ignoreInsecure: true
        });
    }
    await ctx.response.redirect("/api");
});

router.get('/logout', async (ctx) => {
    await ctx.cookies.set('admin', '0');
    await ctx.response.redirect("/");
});

// no iframes
app.use(async (ctx, next) => {
    ctx.response.headers.set('x-frame-options', 'deny');
    await next();
});

app.use(router.routes());
app.use(apiRouter.routes());
app.use(router.allowedMethods());

app.addEventListener('listen', ({ hostname, port, serverType }) => {
    console.log(`"${serverType}" Server listening on https://${hostname}:${port}`)
});

app.listen({ port: 443, hostname: '127.0.0.1' , secure: true, certFile: './certs/cert.crt', keyFile: './certs/cert.key'});