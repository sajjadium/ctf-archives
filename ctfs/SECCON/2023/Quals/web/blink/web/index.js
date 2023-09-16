const app = require("fastify")();
const PORT = 3000;

app.register(require("@fastify/static"), {
  root: require("node:path").join(__dirname, "public"),
});

app.listen({ port: PORT, host: "0.0.0.0" }).catch((err) => {
  app.log.error(err);
  process.exit(1);
});
