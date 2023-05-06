const express = require('express')
const bodyParser = require('body-parser')
const jsonpatch = require('fast-json-patch')
const ejs = require('ejs')
const basicAuth = require('express-basic-auth')


const app = express()

// Middlewares //
app.use(bodyParser.json())
app.use(basicAuth({
    users: { "admin": process.env.SECRET || "admin" },
    challenge: true
}))

/////////////////

let services = {
    status: "online",
    cameras: "online",
    doors: "online",
    dome: "online",
    turrets: "online"
}

// Static folder
app.use("/static", express.static(__dirname + "/static"));

// Homepage
app.get("/", async (req, res) => {
    const html = await ejs.renderFile(__dirname + "/templates/index.ejs", {services})
    res.end(html)
})

// API
app.post("/change_status", (req, res) => {

    let patch = []

    Object.entries(req.body).forEach(([service, status]) => {

        if (service === "status"){
            res.status(400).end("Cannot change all services status")
            return
        }

        patch.push({
            "op": "replace",
            "path": "/" + service,
            "value": status
        })
    });

    jsonpatch.applyPatch(services, patch)

    if ("offline" in Object.values(services)){
        services.status = "offline"
    }

    res.json(services)
})

app.listen(1337, () => {
    console.log(`App listening at port 1337`)
})  