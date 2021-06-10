import * as path from "path";

import express, { NextFunction, Request, Response } from "express";
import * as bodyParser from "body-parser";
import cookieParser from "cookie-parser";

import { MarshalError } from "@zensors/sheriff";

import { SafeError } from "./utils";
import { authRouter } from "./routers/auth";
import { userRouter } from "./routers/user";
import { siteRouter } from "./routers/site";
import { searchRouter } from "./routers/search";

const PORT = Number(process.env.PORT ?? 6284)

const main = async () => {
    const app = express();
    app.use(bodyParser.json());
    app.use(cookieParser())

    app.use("/auth", authRouter.toExpress());
    app.use("/user", userRouter.toExpress());
    app.use("/site", siteRouter.toExpress());
    app.use("/search", searchRouter.toExpress());

    app.use("/", (req, res) => {
        res.sendFile(req.path, { root: path.join(__dirname, "../../client/dist" ) }, (err) => {
            res.sendFile("index.html", { root: path.join(__dirname, "../../client/dist" ) });
        });
    });

    app.use(((error: any, req: Request, res: Response, next: NextFunction) => {
        console.log("Error", error);
        res.status(500);
        if (error instanceof SafeError) {
            res.status(error.code);
            res.json({ error: error.error });
        } else if (error instanceof MarshalError) {
            res.json({ error: error.message });
        } else {
            res.json({ error: "Something went wrong" });
        }
    }) as any)

    app.listen(PORT);
}

main();