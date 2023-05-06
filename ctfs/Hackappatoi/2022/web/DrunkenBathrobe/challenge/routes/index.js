const bot = require("../bot");
const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const window = new JSDOM("").window;
const DOMPurify = createDOMPurify(window);
const storage = {
    //yeah, i'm lazy
    "rum cola": "8",
    mojito: "7",
    "gin tonic": "12",
    spritz: "18",
    negroni: "9",
    "long island": "10",
    caipirinha: "6",
    martini: "7",
    margarita: "9",
};

function secureQuery(string) {
    // let's do this real quick, friends are waiting me at the Drunken Bathrobe
    const reg = /math/gi; // nobody likes math
    let res = string.replaceAll(reg, "");
    res = DOMPurify.sanitize(res);
    return res;
}

async function router(fastify, options) {
    fastify.get("/", async (request, reply) => {
        return reply.sendFile("index.html");
    });

    fastify.get("/search", async (request, reply) => {
        let query = request.query.query;
        console.log("\nSEARCH");
        console.log("query:", query);
        if (query) {
            console.log("there's a query, send msg");
            // query = secureQuery(query);
            // console.log("clean query:", query);
            try {
                let inStorage = storage[query];
                console.log("inStorage:", inStorage);
                if (inStorage) {
                    return reply.view("/templates/search.ejs", {
                        message: "We can make " + inStorage + " more " + query,
                    });
                } else {
                    return reply.view("/templates/search.ejs", {
                        message: "We can't make any " + query + ".\nSorry :(",
                    });
                }
            } catch {
                return reply.view("/templates/search.ejs", {
                    message: "Something went wrong :(",
                });
            }
        } else {
            console.log("no query, return without message");
            return reply.view("/templates/search.ejs", {
                message: null,
            });
        }
    });

    fastify.get("/report", async (request, reply) => {
        return reply.sendFile("report.html");
    });

    fastify.post("/report", async (request, reply) => {
        let { query } = request.body;
        console.log("\nREPORT");
        console.log("original query:", query);
        if (query && typeof query == "string" && query != "") {
            query = secureQuery(query);
            console.log("clean query:", query);
            return bot.checkReport(query).then(() => {
                reply.send({
                    message: "The admin will check the storage ASAP. Thanks!",
                });
            });
        }
        return reply.send({ message: "Missing parameters.", error: 1 });
    });
}

module.exports = () => {
    return router;
};
