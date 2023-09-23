import fastify from 'fastify';
import { JSDOM } from "jsdom";
import fastifyStatic from '@fastify/static';
import path from 'path';
import fastifyFormbody from '@fastify/formbody';

const app = fastify({ logger: true });
const __dirname = path.dirname(new URL(import.meta.url).pathname);

app.register(fastifyStatic, {
    root: path.join(__dirname, 'public')
});
app.register(fastifyFormbody);

app.post("/visit", async (request, reply) => {
    const url = new URL(request.body.url);

    if (url.protocol !== "http:" && url.protocol !== "https:") {
        throw new Error("Invalid protocol");
    }

    const webpage = await fetch(url).then(res => res.text());

    new JSDOM(webpage, {
        runScripts: "dangerously",
    })

    reply.send("the highly optimized admin bot has visited your page!");
});

app.listen({ port: process.env.PORT ?? 3000 });