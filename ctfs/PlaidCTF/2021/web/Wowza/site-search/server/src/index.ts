import * as path from "path";

import express from "express";
import * as fs from "fs-extra";

import { formatTemplate } from "./template";
import { getResults } from "./client";

const PORT = Number(process.env.PORT ?? 6285);
const FLAG = process.env.FLAG ?? "pctf{this_is_a_test_flag}";

const main = () => {
    const app = express();
    app.use("/static", express.static(path.join(__dirname, "../../client/static")));

    app.get("/", async (req, res) => {
        const domain = req.query.domain;
        const query = req.query.q;

        try {
            if (typeof query === "string" && typeof domain === "string") {
                const searchResults = await getResults(domain, query);
                const body = await formatTemplate(domain, searchResults);
                res.type("html").send(body);
                return;
            }
        } catch (e) {
            // pass
        }

        const body = await fs.readFile(path.join(__dirname, "../../client/index.html"));
        res.type("html").send(body);
    });

    app.listen(PORT);


    // Let's just call a spade a spade, shall we?
    const ssrfTarget = express();
    ssrfTarget.get("/flag.txt", (req, res) => {
        if (req.hostname !== "localhost") {
            return res.status(401).send(">:(");
        }

        res.send(FLAG);
    });
    ssrfTarget.listen(1337, "127.0.0.1");
}

main();