const LJSON = require("ljson");

const name = "Powers of 2";
const refUrl = "https://oeis.org/A000079";

/*

map[0] = 1;
for (let i = 0; i < n; i++) {
  map[0] = map[0] * 2;
}
return map[0];

*/

const src = LJSON.stringify(($, map, n) =>
  $(",",
    $(",",
      $("set", map, 0, 1),
      $("for",
        0,
        n,
        i => $("set",
          map,
          0,
          $("*", $("get", map, 0), 2),
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
