const express = require('express')

const app = express();
app.use(express.urlencoded({ extended: true }));

const ADMIN_SECRET = process.env["ADMIN_SECRET"] || "SECRET"
const FLAG = process.env["FLAG"] || "flag{placeholder}"

app.get('/', (req, res)=>{
    let auth = req.headers["authorization"];

    if(auth && auth === ADMIN_SECRET){
        console.log("Hello admin!");
        return res.send(FLAG);
    }
    console.log("Not an admin!");
    return res.send('Not so lucky! ://')
})

app.listen(5000, '0.0.0.0');