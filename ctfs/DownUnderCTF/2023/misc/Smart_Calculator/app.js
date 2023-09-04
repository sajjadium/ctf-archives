#!/usr/bin/env node

const process = require('process')
const readline = require('node:readline/promises');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const flag = process.env.FLAG || "flag{testing}";

const getNumber = (input) => {
    const result = isNaN(Number(input)) ? null : eval(input);
    return result;
};

const calculate = async (op, val1, val2) => {
    switch (op) {
        case "+":
            console.log(`Result: ${val1} + ${val2} = ${getNumber(val1) + getNumber(val2)}\n`);
            break;
        case "-":
            console.log(`Result: ${val1} - ${val2} = ${getNumber(val1) - getNumber(val2)}\n`);
            break;
        case "*":
            console.log(`Result: ${val1} * ${val2} = ${getNumber(val1) * getNumber(val2)}\n`);
            break;
        default:
            if (op in global && val1 + " " + val2 in global[op]) {
                console.error(`Result: ${val1} ${op} ${val2} = ${global[op][val1 + " " + val2]}`);
            } else {
                const restoreFunction = (op) => {
                    global[op] = (op, val1, val2, r) => {
                        try {
                            global[op][val1 + " " + val2] = r;
                            console.error(`Result: ${val1} ${op} ${val2} = ${r}`);
                        } catch (error) {
                            console.error(error);
                        }
                    };

                }

                if (!("operations" in global)) {
                    global["operations"] = [];
                }

                if (!(global["operations"].includes(op))) {
                    console.error("Adding " + op);
                    global["operations"].push(op)
                    restoreFunction(op);
                }

                // Don't want my calculator getting too chunky :)
                if (Object.keys(global[op]).length > 5) {
                    console.error(`Cleaning up "${op}" operation`);
                    delete global[op];
                    restoreFunction(op);
                } else if (global["operations"].length > 5) {
                    for (let i = 0; i < global["operations"].length; i++) {
                        delete global[global["operations"][i]];
                    }
                    global["operations"] = [];
                    restoreFunction(op);
                }

                const result = await rl.question("I've never seen that operation. What should the result be: ");
                global[op](op, val1, val2, result);
            }
    };
}

async function main() {
    let finish = false;
    while (!finish) {
        try {
            const option = await rl.question('Actions:\n1. Calculator\n2. To Decimal\n3. Quit\n> ');
            switch (option) {
                case "1":
                    const op = await rl.question("Choose your operation (+*-) or make your own: ");
                    const val1 = await rl.question("Value 1: ");
                    const val2 = await rl.question("Value 2: ");
                    await calculate(op, val1, val2);
                    break;
                case "2":
                    const number = await rl.question('Give me a number: ');
                    const result = getNumber(number);
                    if (result) {
                        console.log(result.toString() + '\n');
                    } else {
                        console.log("Not a number\n");
                    }
                    break;
                case "3":
                    console.log("Bye bye\n");
                    finish = true;
                    break;
                default:
                    console.log("Invalid option\n");
            }
        } catch (error) {
            console.log("An error has occurred\n");
            console.error("An error has occurred: ", error);
        }
    }
}

main()
