const fs = require("fs");
let filter = null;
try {
    filter = fs.readFileSync("config").toString();
} catch {}

const expr = atob(process.argv.pop());
const regex = new RegExp(filter);
if (regex.test(expr)) {
    console.log("Nop");
} else {
    console.log(eval(expr));
}
