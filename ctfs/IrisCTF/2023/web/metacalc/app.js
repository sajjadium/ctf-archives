const { Sheet } = require('metacalc');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const sheet = new Sheet();

rl.question('I will add 1 to your input?? ', input => {
    sheet.cells["A1"] = 1;
    sheet.cells["A2"] = input;
    sheet.cells["A3"] = "=A1+A2";
    console.log(sheet.values["A3"]);
    process.exit(0);
});
