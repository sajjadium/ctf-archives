# parser.py

VARIABLES = [ "a", "b", "c" ]

def trim_line(line):
    line = line.strip()
    return line

class LeftExpr:
    def __init__(self, var_name):
        if var_name not in VARIABLES:
            raise ValueError()
        self.var_name = var_name

    def validate(self):
        if self.var_name not in VARIABLES:
            raise ValueError()
    
    def __repr__(self):
        return f"LeftExpr({self.var_name})"

RIGHT_EXPR_TYPES = [ "literal", "variable", "arithmetic" ]
ARITHMETIC_OPERATORS = [ "+", "-", "*", "/", "^", "&", "|" ]

class RightExpr:
    def __init__(self, type: str, data: list):
        if type not in RIGHT_EXPR_TYPES:
            raise ValueError()
        self.type = type
        self.data = data
    
    def validate(self):
        if self.type == "literal":
            if len(self.data) != 1 or not isinstance(self.data[0], int):
                raise ValueError()
        elif self.type == "variable":
            if len(self.data) != 1 or self.data[0] not in VARIABLES:
                raise ValueError()
        elif self.type == "arithmetic":
            if len(self.data) != 3:
                raise ValueError()
            op, left, right = self.data
            if op not in ARITHMETIC_OPERATORS:
                raise ValueError()
            if not isinstance(left, RightExpr) or not isinstance(right, RightExpr):
                raise ValueError()
            left.validate()
            right.validate()
    
    def __repr__(self):
        return f"RightExpr({self.type}, {self.data})"

class Parser:
    def __init__(self):
        self.code = []
    
    def parse_line(self, line: str):
        line = trim_line(line)

        if len(line) == 0:
            return

        if "=" not in line:
            raise ValueError()
        lhs, rhs = line.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        left_expr = LeftExpr(lhs)
        right_expr = self.parse_right_expr(rhs)

        self.code.append((left_expr, right_expr))
    
    def parse_primitive(self, token: str):
        if token in VARIABLES:
            return RightExpr("variable", [token])
        
        try:
            value = int(token, 0)
            return RightExpr("literal", [value])
        except ValueError:
            pass

        return None
    
    def parse_right_expr(self, expr: str) -> RightExpr:
        primitive = self.parse_primitive(expr)
        if primitive is not None:
            return primitive

        for op in ARITHMETIC_OPERATORS:
            if op in expr:
                left, right = expr.split(op, 1)
                left = left.strip()
                right = right.strip()
                left_primitive = self.parse_primitive(left)
                right_primitive = self.parse_primitive(right)
                if left_primitive is None or right_primitive is None:
                    raise ValueError()
                return RightExpr("arithmetic", [op, left_primitive, right_primitive])
        else:
            raise ValueError()

    def validate(self):
        for left, right in self.code:
            if not isinstance(left, LeftExpr) or not isinstance(right, RightExpr):
                raise ValueError()
            left.validate()
            right.validate()
