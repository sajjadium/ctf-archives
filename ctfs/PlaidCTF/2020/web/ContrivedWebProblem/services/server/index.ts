import * as path from "path";

import express from "express";
import proxy from "express-http-proxy";
import { Provider } from "nconf";

const nconf = (new Provider())
    .argv()
    .env()
    .defaults({
        "API": "localhost:4101"
    })

export const main = () => {
    const app = express();

    app.get("/dist/main.js", async (req, res) => {
        res.sendFile(path.join(__dirname, "client/dist/main.js"));
    });

    app.use("/api/", proxy(nconf.get("API")) as any);

    app.use("/", async (req, res) => {
        res.sendFile(path.join(__dirname, "client/index.html"));
    });

    app.listen(8080);
};

main();