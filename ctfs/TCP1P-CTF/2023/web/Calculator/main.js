// @deno-types="npm:@types/express"
import express from "npm:express";
import Calculator from "./module/calculator.js"

const app = express()
app.use(express.json())

app.get("/", (_, res) => {
    return res.sendFile("index.html", { root: "." })
})

app.post("/", async (req, res) => {
    const calc = new Calculator()
    const expressions = req.body
    if (!(expressions instanceof Array)) {
        return res.status(400).send("expressions is not a list")
    }
    for (const exp of expressions) {
        calc.addExpression(exp)
    }
    let result = ""
    result = await calc.calculate().catch((e) => { console.error(e); return "something wrong" })
    return res.status(200).send(result.toString())
})

if (import.meta.main) {
    app.listen(8080, "0.0.0.0", () => {
        console.log("listening @ http://0.0.0.0:8080")
    })
}
