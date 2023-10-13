import { f } from "./isolation.js"

class Calculator {
    REGEX_EXPRESSION = /^Math\.[a-zA-Z0-9\._]+$/
    expressions = []

    constructor() {
        this.expressions = []
    }

    addExpression(expression) {
        if (!this.REGEX_EXPRESSION.test(expression)) {
            return false
        }
        this.expressions.push(expression)
        return true
    }

    async calculate() {
        if (this.expressions.length == 0) {
            return "Nothing to calculate"
        }
        let result = ""
        for (const operation of this.expressions) {
            result = `${operation}(${result})`
        }
        return await f(result)
    }
}

export default Calculator
