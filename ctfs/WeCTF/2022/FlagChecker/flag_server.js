const express = require('express')
const fs = require("fs");
const app = express()
const port = 10010
const real_flag = process.env.flag;

function log(data){
    console.log(data)
    fs.writeFileSync("/tmp/log", data + "\n", {flag: "a+"})
}

// give_flag[i] = floor((real_flag[i] + pad[i]) / 2)
function checker(index, flagChar, paddChar, debug=false){
    const lhs = Math.floor(((real_flag[index].charCodeAt(0)%128) + (paddChar.charCodeAt(0)%128)) / 2);
    const rhs = flagChar.charCodeAt(0)%128;
    if (debug) {
        log(`real flag at ${index} is ${real_flag[index]} (${real_flag[index].charCodeAt(0)})`);
        log(`to check flag at ${index} is ${flagChar} (${flagChar.charCodeAt(0)})`);
        log(`pad at ${index} is ${paddChar} (${paddChar.charCodeAt(0)})`);
        log(`lhs=${lhs}, rhs=${rhs}`);
        log(`Are they equal? ${lhs === rhs}`);
    }
    return lhs === rhs
}

app.get('/fake_flag', (req, res) => {
    return res.send(req.query.flag === "we{test}" ? "ok" : "wrong")
})

app.get('/check_flag', (req, res) => {
    const otp = req.query.otp || "";
    const flag = req.query.flag || "";
    const debug = (req.query.debug || "") === "true";
    if (flag.length !== real_flag.length) return res.send("wrong len")
    if (flag.length !== otp.length) return res.send("wrong otp")
    for (let i = 0; i < real_flag.length; i++)
        if (!checker(i, flag[i], otp[i], debug)) return res.send("wrong")
    return res.send("ok")
})


app.listen(port, () => {
    console.log(`App listening on port ${port}`)
})
process.setMaxListeners(0);