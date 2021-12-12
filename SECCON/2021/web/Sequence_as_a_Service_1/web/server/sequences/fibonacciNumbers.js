const LJSON = require("ljson");

const name = "Fibonacci numbers";
const refUrl = "https://oeis.org/A000045";

/*

const map = $("self");
map[0] = 0;
map[1] = 1;
for (let i = 2; i < n+1; i++) {
  map[i] = map[i-1] + map[i-2];
}
return map[n];

*/

const src = LJSON.stringify(($, n) =>
  $(",",
    $(",",
      $(",",
        $("set", $("self"), 0, 0),
        $("set", $("self"), 1, 1),
      ),
      $("for",
        2,
        $("+", n, 1),
        i => $("set",
          $("self"),
          i,
          $("+",
            $("get", $("self"), $("-", i, 1)),
            $("get", $("self"), $("-", i, 2)),
          ),
        ),
      ),
    ),
    $("get", $("self"), n),
  ),
);

module.exports = {
  name,
  src,
  refUrl,
};
