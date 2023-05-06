const fastify = require("fastify")({
    // logger: true,
});
const routes = require("./routes");
const path = require("path");

fastify.register(require("@fastify/formbody"));
fastify.register(require("@fastify/static"), {
    root: path.join(__dirname, "public"),
    prefix: "/",
});
fastify.register(require("@fastify/view"), {
    engine: {
        ejs: require("ejs"),
    },
});
fastify.register(routes());

(async () => {
    fastify.listen({ port: 1337, host: "0.0.0.0" }, (err, address) => {
        if (err) {
            fastify.log.error(err);
            process.exit(1);
        }
        fastify.log.info(`Server listening on ${address}`);
    });
})();
