const readline = require("node:readline/promises");
const vm = require("node:vm");

async function main() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const context = vm.createContext(undefined, {
    codeGeneration: {
      strings: false,
    },
  });

  console.log("Welcome! Please input an expression.");

  while (true) {
    const code = await rl.question("> ");

    if (/[()`]/.test(code)) {
      console.log("You can't call functions!");
      continue;
    }

    try {
      const result = vm.runInContext(code, context);
      console.log(result);
    } catch {
      console.log("Something is wrong...");
    }
  }
}

main();
