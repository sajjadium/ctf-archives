from sympy import *


def parse(expr):
    # learned from our mistake... let's be safe now
    # https://stackoverflow.com/questions/33606667/from-string-to-sympy-expression
    # return sympify(expr)

    # https://docs.sympy.org/latest/modules/parsing.html
    return parse_expr(expr)


print('Welcome to the derivative (with respect to x) solver!')
user_input = input('Your expression: ')
expr = parse(user_input)
deriv = diff(expr, Symbol('x'))
print('The derivative of your expression is:')
print(deriv)
