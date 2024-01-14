import * as parser from "@babel/parser";
import _traverse from "@babel/traverse";
import _generate from "@babel/generator";
const traverse = _traverse.default;
const generate = _generate.default;
import readline from "readline";

class Jail {
  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    this.loopInput();
  }

  async loopInput() {
    while (true) {
      const input = await this.promptForInput();
      this.processInput(input);
    }
  }

  promptForInput() {
    return new Promise((resolve) => {
      this.rl.question("Enter JavaScript code (one line): ", resolve);
    });
  }

  processInput(input) {
    try {
      const ast = this.parseCodeToAST(input);
      const isSafe = this.checkSafe(ast);

      if (!isSafe) {
        throw new Error("Unsafe code detected!");
      }
      const output = this.generateCodeFromAST(ast, input);
      this.evaluateCode(output);
    } catch (error) {
      console.log("Error:", error.message);
    }
  }

  parseCodeToAST(code) {
    return parser.parse(code, {
      sourceType: "module",
      plugins: [],
    });
  }

  checkSafe(ast) {
    return this.noCallExpressions(ast);
  }

  noCallExpressions(ast) {
    let hasCallExpression = false;

    traverse(ast, {
      CallExpression(path) {
        hasCallExpression = true;
        path.stop();
      },
    });

    return !hasCallExpression;
  }

  generateCodeFromAST(ast, originalCode) {
    return generate(ast, {}, originalCode);
  }

  evaluateCode({ code }) {
    try {
      console.log(eval(code));
    } catch (error) {
      console.log("Error evaluating code:", error.message);
    }
  }
}

new Jail();
