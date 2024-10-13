import { get, listen } from "./utils/request.mjs"
import express from "express"

const app = express()

app.get("/", (req, res) => res.send("hello world!"))

app.get("/api/fetch", async (req, res) => {
    if (!req.query.url) {
        return res.status(400).send("url params not found")
    }
    try {
        return res.send(await get(req.query.url, req.query))
    } catch (error) {
        return res.status(500).send("Something Wrong!")
    }
})

listen(app, 8080)
