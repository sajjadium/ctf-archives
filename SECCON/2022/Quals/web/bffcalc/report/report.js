const net = require("node:net");

const BOT_HOST = "bot";
const BOT_PORT = "8000";

const REPORT_DURATION = 30; // secs
const ipToLastTime = new Map(); // (ip: string) -> Time

const router = (fastify, _opts, done) => {
  fastify.post("/", async (req, reply) => {
    const expr = req.body.expr;
    if (expr == null) {
      return reply.code(400).send("expr not found");
    }

    const ip = req.ip;
    const time = Date.now();
    if (ipToLastTime.has(ip)) {
      const diff = (time - ipToLastTime.get(ip)) / 1000; // secs
      const rest = Math.floor(REPORT_DURATION - diff);
      if (rest > 0) {
        return reply.code(400).send(`Please wait ${rest} secs`);
      }
    }
    ipToLastTime.set(ip, time);

    try {
      const client = net.connect(BOT_PORT, BOT_HOST, () => {
        client.write(expr);
      });

      let response = "";
      client.on("data", (data) => {
        response += data.toString();
        client.end();
      });

      client.on("end", () => reply.send(response));
      return reply;
    } catch (e) {
      console.log(e);
      return reply.code(500).send("Something wrong...");
    }
  });

  done();
};

module.exports = router;
