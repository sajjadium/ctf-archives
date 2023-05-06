import * as express from "express";
import * as fs from "fs-extra";
import * as path from "path";
import * as bodyParser from "body-parser";
import { v4 as uuid } from "uuid";

import { startVisiting } from "./page-worker";
import { enqueue } from "./database";

const cacheDir = path.join(__dirname, "../cache");
const clientDir = path.join(__dirname, "../client");

const main = async () => {
    await fs.ensureDir(cacheDir);

    const app = express();
    app.use(bodyParser.json());
    app.use((req, res, next) => {
        res.setHeader("Content-Security-Policy", "script-src 'self' 'unsafe-eval' 'unsafe-inline'");
        next();
    });

    app.get("/", (req, res) => {
        res.sendFile(path.join(clientDir, "index.html"));
    });

    app.post("/upload", async (req, res) => {
        if (typeof req.body !== "object") {
            return res.status(500).send("Bad payload");
        }

        const { type, program } = req.body;
        if (
            typeof type !== "string"
            || type.match(/^[a-zA-Z\-/]{3,}$/) === null
            || typeof program.name !== "string"
            || typeof program.code !== "string"
            || program.code.length > 10000
        ) {
            return res.status(500).send("Invalid program");
        }

        const sanitizedProgram =
            JSON.stringify(program)
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;");

        const template = await fs.readFile(path.join(clientDir, "calculator.hbs"), "utf-8");
        const formattedFile =
            template
                .replace("{{ content-type }}", type)
                .replace("{{ program }}", sanitizedProgram);

        const fileName = `program-${uuid()}`;
        await fs.writeFile(path.join(cacheDir, fileName), formattedFile);

        res.send(`/program/${fileName}`);
    });

    app.post("/report", async (req, res) => {
        if (
            typeof req.body !== "object"
            || typeof req.body.file !== "string"
            || !req.body.file.match(/^program-[a-f0-9-]+$/)
        ) {
            return res.status(500).send("Bad payload");
        }

        const ip = req.ip;
        const { file } = req.body;
        const url = `http://localhost:3838/program/${file}`;

        await enqueue(url, ip)
        res.send("Ok");
    })

    app.get("/program/:file", async (req, res) => {
        const fileName = req.params.file;

        if (fileName.includes("..")) {
            return res.status(500).send("Bad file name");
        }

        const filePath = path.join(cacheDir, fileName);

        res.type("html");
        res.sendFile(filePath);
    });

    app.use("/js", express.static(path.join(clientDir, "js")));
    app.use("/css", express.static(path.join(clientDir, "css")));

    app.listen(3838, () => {
        console.log("Listening on port 3838");
    });
}

startVisiting();
main();


