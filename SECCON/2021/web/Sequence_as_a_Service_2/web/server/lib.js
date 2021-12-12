const lib = {
  "+": (x, y) => x + y,
  "-": (x, y) => x - y,
  "*": (x, y) => x * y,
  "/": (x, y) => x / y,
  ",": (x, y) => (x, y),
  "for": (l, r, f) => {
    for (let i = l; i < r; i++) {
      f(i);
    }
  },
  "set": (map, i, value) => {
    map[i] = value;
    return map[i];
  },
  "get": (map, i) => {
    return typeof i === "number" ? map[i] : null;
  },
};

module.exports = lib;
