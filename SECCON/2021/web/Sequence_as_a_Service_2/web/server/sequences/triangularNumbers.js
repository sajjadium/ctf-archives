const LJSON = require("ljson");

const name = "Triangular numbers";
const refUrl = "https://oeis.org/A000217";

/*

return n * (n + 1) / 2;

*/

const src = LJSON.stringify(($, map, n) =>
  $("/", $("*", n, $("+", n, 1)), 2)
);

module.exports = {
  name,
  src,
  refUrl,
};
