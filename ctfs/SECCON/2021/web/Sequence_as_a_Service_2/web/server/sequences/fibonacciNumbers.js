const LJSON = require("ljson");

const name = "Fibonacci numbers";
const refUrl = "https://oeis.org/A000045";

/*

map[0] = 0;
map[1] = 1;
for (let i = 2; i < n+1; i++) {
  map[i] = map[i-1] + map[i-2];
}
return map[n];

*/

const src = LJSON.stringify(($, map, n) =>
  $(",",
    $(",",
      $(",",
        $("set", map, 0, 0),
        $("set", map, 1, 1),
      ),
      $("for",
        2,
        $("+", n, 1),
        i => $("set",
          map,
          i,
          $("+",
            $("get", map, $("-", i, 1)),
            $("get", map, $("-", i, 2)),
          ),
        ),
      ),
    ),
    $("get", map, n),
  ),
);

module.exports = {
  name,
  src,
  refUrl,
};
