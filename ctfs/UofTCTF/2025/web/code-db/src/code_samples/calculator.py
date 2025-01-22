import operator

def calculate(expression):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    stack = []
    for token in expression.split():
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            result = ops[token](a, b)
            stack.append(result)
        else:
            stack.append(float(token))
    return stack[0]

if __name__ == "__main__":
    expr = input("Enter expression (e.g., 3 4 + 2 *): ")
    print("Result:", calculate(expr))
