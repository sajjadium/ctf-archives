const LJSON = require("ljson");

const name = "Factorial numbers";
const refUrl = "https://oeis.org/A000142";

/*

const map = $("self");
map[0] = 1;
for (let i = 1; i < n + 1; i++) {
  map[0] = map[0] * i;
}
return map[0];

*/

const src = LJSON.stringify(($, n) =>
  $(",",
    $(",",
      $("set", $("self"), 0, 1),
      $("for",
        1,
        $("+", n, 1),
        i => $("set",
          $("self"),
          0,
          $("*", $("get", $("self"), 0), i),
        ),
      ),
    ),
    $("get", $("self"), 0),
  ),
);

module.exports = {
  name,
  src,
  refUrl,
};
