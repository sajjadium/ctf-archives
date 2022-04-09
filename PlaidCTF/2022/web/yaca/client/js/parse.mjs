/*
Operation precedences:
   0: exponentiation
   1: implicit multiplication
   2: multiplication/division
   3: unary operators
   4: addition/subtraction
*/


// We could probably have lexed directly into the parse token, but
// this way we keep a bit more separation of church & state
const lexTokenToParseToken = (token) => {
    if (token === undefined) {
        return { kind: "EOF" };
    }

    switch (token.kind) {
        case "operator": {
            switch (token.value) {
                case "invert":   return { kind: "UNOP", value: token.value, precedence: 3, isOp: true };
                case "subtract": return { kind: "MAYBE_UNOP", value: token.value, unopValue: "negate", precedence: 4, isOp: true };
                case "exponent": return { kind: "BINOP", value: token.value, precedence: 0, isOp: true, };
                case "multiply": return { kind: "BINOP", value: token.value, precedence: 2, isOp: true, };
                case "divide":   return { kind: "BINOP", value: token.value, precedence: 2, isOp: true, };
                case "add":      return { kind: "BINOP", value: token.value, precedence: 4, isOp: true, };
                default: throw new Error(`Unknown operator ${token.value}`);
            }
        }
        case "open-paren": return { kind: "EXPR_START" };
        case "close-paren": return { kind: "EXPR_END" };
        case "number": return { kind: "VALUE", ast: { kind: "number", value: token.value } };
        case "variable": return { kind: "VALUE", ast: { kind: "variable", variable: token.value } };
        default: throw new Error(`Unknown token kind ${token.kind}`);
    }
}

const mightBeUnop = (token) => {
    return (
        token.kind === "UNOP"
        || token.kind === "MAYBE_UNOP"
        || token.kind === "FUNCTION"
        || token.kind === "IMPLICIT_MULTIPLICATION"
    );
}

const mightBeBinop = (token) => {
    return (
        token.kind === "BINOP"
        || token.kind === "MAYBE_UNOP"
    );
}

const parseOne = (stack, lookahead) => {
    // If we can reduce a parenthetical expression, we want to
    if (stack[0]?.kind === "EXPR_END") {
        const [_end, value, _start, ...rest] = stack;

        if (stack[1]?.kind !== "VALUE" || stack[2]?.kind !== "EXPR_START") {
            throw new Error("Received unexpected close parenthesis");
        }

        return ["reduce", [value, ...rest]];
    }

    // Otherwise, all of our reductions occur on values
    if (stack[0]?.kind === "VALUE") {
        // We have some special cases for two adjacent values, when the first one is
        // a pure variable (function call) or number (term multiplication)
        if (lookahead.kind === "VALUE" || lookahead.kind === "EXPR_START") {
            if (stack[0].ast.kind === "variable") {
                const [token, ...rest] = stack;
                const newToken = {
                    kind: "FUNCTION",
                    isOp: true,
                    precedence: 3,
                    name: token.ast.variable
                }

                const newStack = [newToken, ...rest];
                return ["reduce", newStack];
            }

            if (stack[0].ast.kind === "number") {
                const [token, ...rest] = stack;
                const newToken = {
                    kind: "IMPLICIT_MULTIPLICATION",
                    isOp: true,
                    precedence: 1,
                    value: token.ast.value
                }

                const newStack = [newToken, ...rest];
                return ["reduce", newStack];
            }
        }

        // If we have an operator on our stack, we want to reduce it unless the upcoming
        // operator has a stronger precedence
        if (stack[1]?.isOp) {
            const shouldShift = mightBeBinop(lookahead) && lookahead.precedence < stack[1].precedence;
            if (shouldShift) {
                return ["shift"];
            }

            const isBinop = mightBeBinop(stack[1]) && stack[2]?.kind === "VALUE";

            if (isBinop) {
                const [right, binop, left, ...rest] = stack;

                // Binops are easy
                const newValue = {
                    kind: "VALUE",
                    ast: {
                        kind: "binop",
                        op: binop.value,
                        values: [
                            left.ast,
                            right.ast,
                        ]
                    }
                };

                return ["reduce", [newValue, ...rest]]
            }

            const isUnop = mightBeUnop(stack[1]);
            if (!isUnop) {
                throw new Error("Unexpected operator");
            }

            const [value, unop, ...rest] = stack;
            let newToken;

            // Handle each of the different types of unary operators
            switch (unop.kind) {
                case "UNOP":
                case "MAYBE_UNOP": {
                    const op = unop.kind === "MAYBE_UNOP" ? unop.unopValue : unop.value;
                    newToken = {
                        kind: "VALUE",
                        ast: {
                            kind: "unop",
                            op,
                            value: value.ast
                        }
                    };
                    break;
                }
                case "FUNCTION": {
                    newToken = {
                        kind: "VALUE",
                        ast: {
                            kind: "function",
                            name: unop.name,
                            argument: value.ast,
                        }
                    };
                    break;
                }
                case "IMPLICIT_MULTIPLICATION": {
                    newToken = {
                        kind: "VALUE",
                        ast: {
                            kind: "binop",
                            op: "multiply",
                            values: [
                                { kind: "number", value: unop.value },
                                value.ast,
                            ]
                        }
                    };
                    break
                }
                default: {
                    throw new Error(`Unknown unary operator: ${unop.kind}`);
                }
            }

            return ["reduce", [newToken, ...rest]];
        }
    }

    // Otherwise, we have no reductions to do, so we shift in a new token
    return ["shift"];
}


export default (tokens) => {
    const queue = [...tokens];
    let stack = [];

    const maxIter = 1000;
    let iter = 0;

    while (queue.length > 0 || stack.length > 1) {
        // I haven't proven that this terminates so uh
        // Hopefully this will keep me from nuking anyone's chrome
        if (iter >= maxIter) {
            throw new Error("Timeout");
        }
        iter++;

        const lookahead = lexTokenToParseToken(queue[0]);
        const action = parseOne(stack, lookahead);

        if (window.DEBUG) {
            console.log([...stack], lookahead, action);
        }

        switch (action[0]) {
            case "shift": {
                if (lookahead.kind === "EOF") {
                    throw new Error("Attempting to shift EOF, which indicates a malformed program");
                }

                queue.shift();
                stack = [lookahead, ...stack]
                break;
            }
            case "reduce": {
                stack = action[1];
            }
        }
    }

    // If we parsed correctly, we should be left with a single value
    // representing our final result
    if (stack[0]?.kind !== "VALUE") {
        throw new Error("Parser did not return a value");
    }

    return stack[0].ast;
}