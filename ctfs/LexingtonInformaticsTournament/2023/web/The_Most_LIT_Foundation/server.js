import url from "url";
import path from "path";

import Fastify from "fastify";
import fastifyStatic from "@fastify/static";

import api from "./routes/api.js";

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));

const fastify = Fastify({ logger: true });

fastify.register(fastifyStatic, {
    root: path.join(__dirname, "./public/"),
    redirect: true,
});

fastify.register(api, {
    prefix: "/api",
});

await fastify.listen({ port: 5753 });
