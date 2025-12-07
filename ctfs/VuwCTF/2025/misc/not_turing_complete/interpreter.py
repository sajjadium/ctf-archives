# interpreter.py

from parser import VARIABLES, ARITHMETIC_OPERATORS, LeftExpr, RightExpr

class Interpreter:
    def __init__(self, code: list):
        self.code = code
        self.variables = { var: 0 for var in VARIABLES }

    def initialize(self, a_value: int = 0, b_value: int = 0, c_value: int = 0):
        self.variables['a'] = a_value
        self.variables['b'] = b_value
        self.variables['c'] = c_value

    def interpret(self):
        for lhs, rhs in self.code:
            value = self.evaluate_right_expr(rhs)
            self.variables[lhs.var_name] = value
    
    def evaluate_right_expr(self, expr: RightExpr) -> int:
        if expr.type == "literal":
            literal_value = expr.data[0]
            return literal_value
        elif expr.type == "variable":
            var_name = expr.data[0]
            return self.variables[var_name]
        elif expr.type == "arithmetic":
            op, left_expr, right_expr = expr.data
            left_value = self.evaluate_right_expr(left_expr)
            right_value = self.evaluate_right_expr(right_expr)

            if op == "+":
                return left_value + right_value
            elif op == "-":
                return left_value - right_value
            elif op == "*":
                return left_value * right_value
            elif op == "/":
                return left_value // right_value
            elif op == "^":
                return left_value ^ right_value
            elif op == "&":
                return left_value & right_value
            elif op == "|":
                return left_value | right_value
            else:
                raise ValueError()
        else:
            raise ValueError()