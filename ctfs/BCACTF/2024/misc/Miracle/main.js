const readline = require("readline");
const fs = require("fs");

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// thanks chatgpt
function printWithoutNewline(text) {
  process.stdout.write(text);
}

function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}
//end thanks chatgpt

const flag = fs.readFileSync("flag.txt", "utf8");

async function run() {
  const name = await prompt("What is your name?\n") ?? "Harry";
  const ans = await prompt("What is 55+22?\n") ?? "0";
  if (eval("Number(ans)") === 77) {
    console.log("Correct!");
    console.log("Waiting for bits to flip...");
    for (let i = 0; i < 10; i++) {
      printWithoutNewline("...");
      await sleep(300);
    }
    console.log("\n");
    if (eval(ans) === 63) {
      console.log(`You made those bits flip?? You're a wizard ${name}! `);
      console.log(`Here's your flag: ${flag}`);
    } else {
        console.log("You didn't make the bits flip. Too bad ");
    }
  } else {
    console.log("wow you suck at math.");
  }
  process.exit(1);
}

run();