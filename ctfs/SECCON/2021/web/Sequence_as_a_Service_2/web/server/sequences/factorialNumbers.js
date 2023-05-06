const LJSON = require("ljson");

const name = "Factorial numbers";
const refUrl = "https://oeis.org/A000142";

/*

map[0] = 1;
for (let i = 1; i < n + 1; i++) {
  map[0] = map[0] * i;
}
return map[0];

*/

const src = LJSON.stringify(($, map, n) =>
  $(",",
    $(",",
      $("set", map, 0, 1),
      $("for",
        1,
        $("+", n, 1),
        i => $("set",
          map,
          0,
          $("*", $("get", map, 0), i),
        ),
      ),
    ),
    $("get", map, 0),
  ),
);

module.exports = {
  name,
  src,
  refUrl,
};
