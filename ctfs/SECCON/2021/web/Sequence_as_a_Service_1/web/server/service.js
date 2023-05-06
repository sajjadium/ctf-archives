const LJSON = require("ljson");
const lib = require("./lib.js");

const sequence = process.argv[2];
const n = parseInt(process.argv[3]);

console.log(LJSON.parseWithLib(lib, sequence)(n));
