const LJSON = require("ljson");
const lib = require("./lib.js");

const sequence0 = process.argv[2];
const n0 = parseInt(process.argv[3]);
const sequence1 = process.argv[4];
const n1 = parseInt(process.argv[5]);

console.log([
  LJSON.parseWithLib(lib, sequence0)({}, n0),
  LJSON.parseWithLib(lib, sequence1)({}, n1),
]);
