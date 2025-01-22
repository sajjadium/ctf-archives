import * as parser from "@babel/parser";
import _traverse from "@babel/traverse";
import _generate from "@babel/generator";
import * as _minify from "babel-minify";
const minify = _minify.default;
const traverse = _traverse.default;
const generate = _generate.default;
import readline from "readline";

class Jail {
  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    this.getInput();
  }

  async getInput() {
    const kvPair = await this.promptForInput('Enter key value pair ["key","value"]: ');
    const kvPairObj = this.parseKvPair(kvPair);
    if (!kvPairObj) {
      this.rl.close();
      return;
    }
    const helper = await this.promptForInput('Enter helper method: ');
    if (!this.isSafeHelper(helper)) {
      this.rl.close();
      return;
    }
    const code = await this.promptForInput("Enter JavaScript code (one line): ");
    this.processInput(code, kvPairObj, helper);
    this.rl.close();
  }

  isSafeHelper(weapon) {
    const BLACKLISTED = ["replace", "replaceAll"]; // js evaluator ptsd
    if (weapon in String.prototype && !(weapon in Object.prototype) && !BLACKLISTED.includes(weapon)) {
      return weapon;
    }
    console.log("Invalid helper method");
    return null;
  }

  promptForInput(prompt) {
    return new Promise((resolve) => {
      this.rl.question(prompt, resolve);
    });
  }

  parseKvPair(kvPairStr) {
    try {
      const parsed = JSON.parse(kvPairStr);
      if (!Array.isArray(parsed) || parsed.length !== 2 || typeof parsed[0] !== "string" || !["string", "number", "boolean"].includes(typeof parsed[1])) {
        throw new Error("Invalid key value pair");
      }
      return {
        [parsed[0]]: parsed[1],
      }
    } catch (error) {
      console.log("Error parsing key value pair:", error.message);
      return null
    }
  }

  minifyCode(code) {
    try {
      const result = minify(code, {});
      if (result.error) {
        throw result.error;
      }
      return result
    } catch (error) {
      throw new Error("Error during minification: " + error.message);
    }
  }

  processInput(code, kvPairObj, helper) {
    try {
      const ast = this.parseCodeToAST(code, kvPairObj)
      const isSafe = this.checkSafe(ast);

      if (!isSafe) {
        throw new Error("Unsafe code detected!");
      }
      const { code: codeToEval } = this.generateCodeFromAST(ast, code);
      this.evaluateCode(codeToEval, helper);
    } catch (error) {
      console.log("Error:", error.message);
    }
  }

  parseCodeToAST(code, kvPairObj) {
    return parser.parse(code, {
      ...kvPairObj,
      attachComment: false,
      sourceType: "module",
      plugins: [],
    });
  }

  checkSafe(ast) {
    return this.noBlacklistedNodes(ast) && this.isStaticallyEvaluable(ast);
  }

  noBlacklistedNodes(ast) {
    let failed = false;
    let numCalls = 0;
    traverse(ast, {
      CallExpression(path) {
        numCalls++;
        const callee = path.get("callee");
        if (!callee.isIdentifier({ name: "__HELPER__" }) || numCalls > 1) {
          failed = true;
          path.stop();
        }
      },
      "Literal|OptionalCallExpression|ObjectExpression|FunctionExpression|Import|TaggedTemplateExpression|TemplateElement|UnaryExpression|AssignmentExpression|OptionalMemberExpression|SpreadElement|ArrayExpression|NewExpression|Declaration|FunctionDeclaration|MemberExpression|ArrowFunctionExpression|DebuggerStatement|RestElement|WithStatement"(
        path
      ) {
        console.log("Blacklisted node detected:", path.type);
        failed = true;
        path.stop();
      }
    });

    return !failed;
  }

  isStaticallyEvaluable(ast) {
    let isConfident = true;
    traverse(ast, {
      Program(path) {
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
    return this.minifyCode(generate(ast, {}, originalCode).code);
  }

  evaluateCode(code, helper) {
    try {
      const newCode = `
      const __HELPER__ = function (str, ...args){
            if (typeof str !== "string") return
            return str["${helper}"](...args)
      }; 
      ${code}`
      eval(newCode);
    } catch (error) {
      console.log("Error evaluating code:", error.message);
    }
  }
}

new Jail();
