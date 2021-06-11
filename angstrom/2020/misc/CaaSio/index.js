const readline = require("readline");
const util = require("util");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
let reg = /(?:Math(?:(?:\.\w+)|\b))|[()+\-*/&|^%<>=,?:]|(?:\d+\.?\d*(?:e\d+)?)/g
console.log("Welcome to my Calculator-as-a-Service (CaaS)!");
console.log("Our advanced js-based calculator allows for advanced boolean-based operations!");
console.log("Try calculating '(2 < 3) ? 5 : 6' (without the quotes of course)!");
console.log("However, if we don't trust you then we'll have to filter your input a bit.");
function question(q) {
    return new Promise((res, rej) => rl.question(q, res));
}
// don't want you modifying the Math object
Object.freeze(global);
Object.freeze(Math);

const user = {};
async function main() {
    const name = await question("What's your name? ");
    if (name.length > 10) {
        console.log("Your name is too long, I can't remember that!");
        return;
    }
    user.name = name;
    if (user.name == "such_a_trusted_user_wow") {
        user.trusted = true;
    }
    user.queries = 0;
    console.log(`Hello ${name}!`);
    while (user.queries < 3) {
        user.queries ++;
        let prompt = await question("> ");
        if (prompt.length > 200) {
            console.log("That's way too long for me!");
            continue;
        }
        if (!user.trusted) {
            prompt = (prompt.match(reg) || []).join``;
        }
        try {
            console.log(eval(prompt));
        } catch (err) {
            console.log("There has been an error! Oh noes!");
        }
    }
    console.log("I'm afraid you've run out of queries.");
    console.log("Goodbye!");
}
setTimeout(function() {
    console.log("Time's up!");
    console.log("Goodbye!");
    process.exit(0);
}, 60000);
main();