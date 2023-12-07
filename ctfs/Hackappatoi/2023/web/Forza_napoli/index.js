const bot = require("../bot");

function isValidUrl(url) {
    let regex = /^(http|https):\/\/(www\.){0,1}forzanapoli.hackappatoi.com/i;
    return regex.test(url) && !url.includes("@");
}

async function router(fastify, options) {
    fastify.get("/", async (request, reply) => {
        return reply.sendFile("index.html");
    });

    fastify.get("/share", async (request, reply) => {
        return reply.sendFile("share.html");
    });

    fastify.post("/share", async (request, reply) => {
        let { url } = request.body;
        console.log("\nSHARE");
        console.log("original url:", url);
        if (url && typeof url == "string" && url != "") {
            let valid = isValidUrl(url);
            console.log("valid url:", valid);
            if (valid) {
                bot.checkUrl(url); // Set the cookies and visit url
                return reply.view("/templates/success.ejs", { message: "The admin will check your link ASAP. Thanks!" });
            } else {
                return reply.view("/templates/success.ejs", { message: "Invalid URL! You are not a real Napoli fan 😡" });
            }
        }
        return reply.code(400).type("text/html").view("/templates/error.ejs", {
            code: 400,
            message: "Missing parameters :(",
        });
    });

    fastify.setNotFoundHandler((request, reply) => {
        reply.code(404).type("text/html").view("/templates/error.ejs", {
            code: 404,
            message: "Page not found :(",
        });
    });
}

module.exports = () => {
    return router;
};
