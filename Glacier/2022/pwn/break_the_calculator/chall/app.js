const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});


function calculate(formula) {
    const parsedFormula = formula.replace(/\s/g, "");
    if(parsedFormula.match(/^[^a-zA-Z\s]*$/)) {
        const result = Function('return ' + parsedFormula)();
        console.log("Result: " + result + " - GoodBye");
    } else {
        console.log("Don't hack here - GoodBye!");
    }
    rl.close();
    process.exit(0)
}

try {
    console.log("Welcome to my Calculator! Please type in formula:")
    rl.on('line', (line) => {
        calculate(line);
    });
} catch(e) {}


