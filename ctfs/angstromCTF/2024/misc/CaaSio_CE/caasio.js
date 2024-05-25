#!/usr/local/bin/node

const readline = require("readline/promises");
const rl = readline.createInterface({input: process.stdin, output: process.stdout});

console.log("Welcome to CaaSio: Contrived Edition!");
console.log("What \"math\" expression would you like to evaluate?");
rl.question("> ")
    .then(inp => {
        if (inp.length > 200) {
            console.log("That's so much math; what do you think I am, a calculator???");
            throw new Error();
        }
        const banned = new Set(".,:;(){}<>`pxu");
        for (const char of inp) {
            const c = char.charCodeAt(0);
            if (c < 0x20 || c > 0x7e || banned.has(char)) {
                console.log("I have arbitrarily deemed your input to not be math.");
                throw new Error();
            }
        }
        return inp;
    })
    .then(inp => console.log(Function("return " + inp)()))
    .catch((e) => console.log("Bye!", e))
    .finally(() => rl.close());
