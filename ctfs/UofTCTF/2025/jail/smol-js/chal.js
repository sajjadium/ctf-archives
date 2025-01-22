import * as parser from "@babel/parser";
import _traverse from "@babel/traverse";
import _generate from "@babel/generator";
import * as _minify from "babel-minify";
import readline from "readline";
const minify = _minify.default;
const traverse = _traverse.default;

class Jail {
    constructor() {
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
        });
        this.promptForInput().then((input) => {
            this.processInput(input);
            this.rl.close();
        });
    }

    promptForInput() {
        return new Promise((resolve) => {
            this.rl.question("Enter JavaScript code (one line): ", resolve);
        });
    }

    processInput(input) {
        try {
            const unminifiedCode = input;
            const parsedAst = this.parseCodeToAST(unminifiedCode);
            const isSafe = this.noBadNodes(parsedAst);

            if (!isSafe) {
                throw new Error("Unsafe code detected!");
            }
            // I'll help you make smol code :)
            const {
                code: minifiedCode
            } = this.minifyCode(unminifiedCode);
            if (!minifiedCode || minifiedCode.length === 0) {
                throw new Error("Minified code is empty");
            }
            const codeToEvaluate = this.chooseCode(unminifiedCode, minifiedCode);
            if (codeToEvaluate.length > 23) {
                console.log("not smol enough");
                return;
            }
            try {
                eval(codeToEvaluate);
            } catch {
                console.log("Error during evaluation");
            }
        } catch (error) {
            console.log("Error:", error.message);
        }
    }

    chooseCode(code1, code2) {
        return code1.length < code2.length ? code1 : code2;
    }

    parseCodeToAST(code) {
        return parser.parse(code, {
            sourceType: "module",
            plugins: [],
        });
    }

    noBadNodes(ast) {
        let hasBadNodes = false;

        traverse(ast, {
            "CallExpression|AssignmentExpression"(path) {
                hasBadNodes = true;
                path.stop();
            },
        });

        return !hasBadNodes;
    }

    minifyCode(code) {
        try {
            const result = minify(code, {});
            if (result.error) {
                throw result.error;
            }
            return result;
        } catch (error) {
            throw new Error("Error during minification: " + error.message);
        }
    }
}

new Jail();