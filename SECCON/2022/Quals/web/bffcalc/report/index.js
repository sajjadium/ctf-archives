const fastify = require("fastify")({ trustProxy: true });

const PORT = "3000";

fastify.register(require("@fastify/formbody"));
fastify.register(require("./report"), { prefix: "/report" });

fastify.listen({ port: PORT, host: "0.0.0.0" }, (err, address) => {
  if (err) {
    fastify.log.error(err);
    process.exit(1);
  }
  console.log(`Server listening at "${address}"`);
});
