// flag in ./flag.txt

const acorn = require("acorn");
const vm = require("vm");
const readline = require("readline");

const interface = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

const legalVariables = new Set(["a", "b", "c", "x", "y", "z"]);

function len(expr) {
    return expr.end - expr.start;
}

function isValidExpression(
    expr,
    ctx = {
        seenArray: false,
        seenObject: false,
        seenSequence: false,
    }
) {
    switch (expr.type) {
        case "ArrayExpression":
            if (ctx.seenArray) {
                return false;
            }
            ctx.seenArray = true;
            if (expr.elements.length > 3) {
                return false;
            }
            return expr.elements.every(
                (ele) =>
                    !ele ||
                    (len(ele) < 50 && isValidExpression(ele, ctx))
            );
        case "ObjectExpression":
            if (ctx.seenObject) {
                return false;
            }
            ctx.seenObject = true;
            if (expr.properties.length > 3) {
                return false;
            }
            return expr.properties.every(
                (prop) =>
                    len(prop.key) < 50 &&
                    isValidExpression(prop.value, ctx)
            );
        case "UnaryExpression":
        case "UpdateExpression":
            return isValidExpression(expr.argument, ctx);
        case "BinaryExpression":
        case "LogicalExpression":
            return (
                isValidExpression(expr.left, ctx) &&
                isValidExpression(expr.right, ctx)
            );
        case "AssignmentExpression":
            return (
                expr.left.type === "Identifier" &&
                legalVariables.has(expr.left.name, ctx) &&
                isValidExpression(expr.right, ctx)
            );
        case "MemberExpression":
            return (
                isValidExpression(expr.object, ctx) &&
                (expr.property.type === "Literal" ||
                    expr.property.type === "Identifier")
            );
        case "ConditionalExpression":
            return (
                isValidExpression(expr.test, ctx) &&
                isValidExpression(expr.alternate, ctx) &&
                isValidExpression(expr.consequent, ctx)
            );
        case "CallExpression":
            return (
                expr.callee.type === "MemberExpression" &&
                expr.callee.object.type === "Identifier" &&
                expr.callee.object.name === "Math" &&
                expr.callee.property.type === "Identifier" &&
                expr.arguments.every((arg) => isValidExpression(arg, ctx))
            );
        case "SequenceExpression":
            if (ctx.seenSequence) {
                return false;
            }
            ctx.seenSequence = true;
            if (expr.expressions.length > 3) {
                return false;
            }
            return expr.expressions.every((x) => isValidExpression(x, ctx));
        case "Literal":
            return len(expr) < 50;
        case "Identifier":
            return legalVariables.has(expr.name);
        default:
            return false;
    }
}

function isValid(str) {
    try {
        if (
            ["__", "eval", "constructor", "prototype"].some((x) =>
                str.includes(x)
            )
        ) {
            return false;
        }
        if (str.length > 240) {
            return false;
        }
        const abstractSnakeTree = acorn.parse(str, { ecmaVersion: "latest" });
        if (abstractSnakeTree.body.length !== 1) {
            return false;
        }
        const stmt = abstractSnakeTree.body[0];
        if (stmt.type !== "ExpressionStatement") {
            return false;
        }
        return isValidExpression(stmt.expression);
    } catch (e) {
        return false;
    }
}

interface.question(
    "Welcome to CaaSio Snake Edition! Enter your calculation:\n",
    function (input) {
        interface.close();
        if (isValid(input)) {
            try {
                const ctx = Object.create(null);
                const val = vm.runInNewContext(input, ctx);
                console.log("Result:");
                console.log(val);
                console.log("Variables:");
                for (const variable of legalVariables) {
                    if (variable in ctx) {
                        console.log(variable, "=", ctx[variable]);
                    }
                }
            } catch (e) {
                console.log("err I'm not getting hacked this time >:(((((");
            }
        } else {
            console.log("I'm not getting hacked this time >:(((((");
        }
    }
);
