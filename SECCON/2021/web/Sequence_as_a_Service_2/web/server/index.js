const fastify = require("fastify")();
const execFile = require("util").promisify(require("child_process").execFile);
const fs = require("fs");

const PORT = process.env.PORT || process.exit(1);

const sequences = JSON.stringify([
  require("./sequences/powersOfTwo"),
  require("./sequences/triangularNumbers"),
  require("./sequences/factorialNumbers"),
  require("./sequences/fibonacciNumbers"),
  require("./sequences/lucasNumbers"),
]);

const indexHtml = fs.readFileSync("./index.html").toString();
fastify.get("/", async (request, reply) => {
  reply.type("text/html; charset=UTF-8").send(indexHtml);
});

fastify.get("/api/getValue", async (request, reply) => {
  const sequence0 = request.query.sequence0;
  const n0 = request.query.n0;
  const sequence1 = request.query.sequence1;
  const n1 = request.query.n1;
  if (sequence0 == null || n0 == null || sequence1 == null || n1 == null) {
    reply.code(400).send("Invalid params");
    return;
  }

  try {
    const result = await execFile(
      "node",
      ["./service.js", sequence0, n0, sequence1, n1],
      {
        timeout: 1000,
      }
    );
    reply
      .header("Content-Type", "application/json; charset=utf-8")
      .send(result.stdout);
  } catch (err) {
    reply.statusCode = 500;
    if (err.killed) {
      reply.send("Timeout");
    } else {
      reply.send("Something wrong");
    }
  }
});

fastify.get("/sequences.json", async (request, reply) => {
  reply.type("application/json").send(sequences);
});

fastify
  .listen(PORT, "0.0.0.0")
  .then((address) => console.log(`Server listening on ${address}`))
  .catch((err) => {
    fastify.log.error(err);
    process.exit(1);
  });
