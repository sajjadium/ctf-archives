"use strict";

const jwt = require("jsonwebtoken");
const express = require("express");
const vm = require("vm");

const app = express();

const PORT = process.env.PORT || 12345;

app.use(express.urlencoded({ extended: false }));

const ctx = { codeGeneration: { strings: false, wasm: false }};
const unserialize = (data) => new vm.Script(`"use strict"; (${data})`).runInContext(vm.createContext(Object.create(null), ctx), { timeout: 250 });

process.mainModule = null; // 🙃

app.use(express.static("public"));

app.post("/api/verify", (req, res) => {
    let { token, secretOrPrivateKey } = req.body;
    try {
        token = unserialize(token);
        secretOrPrivateKey = unserialize(secretOrPrivateKey);
        res.json({
            success: true,
            data: jwt.verify(token, secretOrPrivateKey)
        });
    }
    catch {
        res.json({
            success: false,
            data: "Verification failed"
        });
    }
});

app.listen(PORT, () => console.log(`web/jwtjail listening on port ${PORT}`));