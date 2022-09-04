const fs = require("fs");
const { argv } = require("process");
const bytes = fs.readFileSync("propaganda.wasm");

WebAssembly.instantiate(bytes, {}).then((Module) => {
  x = Module.instance.exports.f(BigInt(argv[2]));
  console.log(BigInt.asUintN(64, x));
});

