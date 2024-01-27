const circomlibjs = require("circomlibjs")
const snarkjs = require("snarkjs");
const fs = require("fs");
const express = require('express')

let digest = ""
let vkey = {}

async function setup() {
    const flag = await fs.readFileSync("secret/flag.txt");
    const preimage = '0x' + flag.subarray(7, flag.length - 1).toString('hex');
    const poseidon = await circomlibjs.buildPoseidon();
    digest = poseidon.F.toString(poseidon([preimage]));
    vkey = JSON.parse(fs.readFileSync("build/verification_key.json", 'utf8'));
}

const app = express()
app.use(express.json());
const PORT = 31338

app.get('/public', (req, res) => {
    res.send([digest])
})

app.post('/submit-proof', async (req, res) => {
    try {
        const ok = await snarkjs.plonk.verify(vkey, [digest], req.body)
        if (ok === true) {
            res.send(fs.readFileSync("secret/flag.txt", 'utf8'))
            console.log(new Date(), req.body)
        } else {
            res.send("Nice try!")
        }
    } catch (err) {
        res.send(err.toString())
    }
})

setup().then(() => {
    app.listen(PORT, () => {
        console.log("ON!")
    })
})
