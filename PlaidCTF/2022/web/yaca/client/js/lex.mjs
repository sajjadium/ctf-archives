export default (source) => {
    let index = 0;
    const tokens = [];

    while (index < source.length) {
        const token = source[index];
        index += 1;

        switch (token) {
            case ' ':
            case '\t':
            case '\n':
            case '\r':
                break;
            case "~":
            case "+":
            case "-":
            case "*":
            case "/":
            case "^": {
                const op =
                    token === "~" ? "invert" :
                    token === "+" ? "add" :
                    token === "-" ? "subtract" :
                    token === "*" ? "multiply" :
                    token === "/" ? "divide" :
                    token === "^" ? "exponent" :
                    null;

                tokens.push({
                    kind: "operator",
                    value: op,
                });
                break
            }
            case "(":  {
                tokens.push({
                    kind: "open-paren",
                });
                break;
            }
            case ")":  {
                tokens.push({
                    kind: "close-paren",
                });
                break;
            }
            default: {
                if (token.match(/^[0-9\.]$/)) {
                    let currentToken = token;

                    while (index < source.length && source[index].match(/^[0-9\.]$/)) {
                        currentToken += source[index];
                        index += 1;
                    }

                    const value = Number(currentToken);
                    tokens.push({
                        kind: "number",
                        value,
                    });
                    break;
                }

                if (token.match(/^[a-z]$/)) {
                    let currentToken = token;

                    while (index < source.length && source[index].match(/^[a-z0-9_]$/)) {
                        currentToken += source[index];
                        index += 1;
                    }

                    tokens.push({
                        kind: "variable",
                        value: currentToken,
                    });
                    break;
                }

                throw new Error(`Syntax error: Unexpected "${token}"`)
            }
        }
    }

    return tokens;
}
