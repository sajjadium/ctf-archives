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
      // oops no eval() here lol
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
    return this.isStaticallyEvaluable(ast);
  }

  isStaticallyEvaluable(ast) {
    let isConfident = true;
    traverse(ast, {
      Program(path) {
        // Check if every node in the body is an expression wrapper and can be evaluated statically with confidence
        const body = path.get("body");

        for (const node of body) {
          if (!node.isExpressionWrapper()) {
            isConfident = false;
            break;
          }

          const { confident } = node.evaluate();
          if (!confident) {
            isConfident = false;
            break;
          }
        }

        path.stop();
      },
    });

    return isConfident;
  }

  generateCodeFromAST(ast, originalCode) {
    return generate(ast, {}, originalCode);
  }
}

new Jail();
