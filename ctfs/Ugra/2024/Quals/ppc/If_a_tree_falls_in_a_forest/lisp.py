from functools import reduce
import operator
import os
import resource
import sys
import yaml


sys.setrecursionlimit(2 ** 31 - 1)
resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
resource.setrlimit(resource.RLIMIT_DATA, (10000000, 10000000))
resource.setrlimit(resource.RLIMIT_STACK, (10000000, 10000000))


class DelayedInterpret:
    def __init__(self, ctx, prog):
        self.ctx = ctx
        self.prog = prog


nil = []

base_ctx = {
    "nil": nil,
    "+": lambda ctx, *args: sum((interpret(ctx, arg) for arg in args), 0),
    "-": lambda ctx, a, b: interpret(ctx, a) - interpret(ctx, b),
    "quote": lambda ctx, arg: arg,
    "list": lambda ctx, *args: [interpret(ctx, arg) for arg in args],
    "if": lambda ctx, cond, then, else_: DelayedInterpret(ctx, then if interpret(ctx, cond) != nil else else_),
    "lambda": lambda lctx, names, expr: lambda cctx, *largs: DelayedInterpret(lctx | {name: interpret(cctx, larg) for name, larg in zip(names, largs)}, expr),
    "eq": lambda ctx, a, b: True if interpret(ctx, a) == interpret(ctx, b) else nil,
    "lt": lambda ctx, a, b: True if interpret(ctx, a) < interpret(ctx, b) else nil,
    "gt": lambda ctx, a, b: True if interpret(ctx, a) > interpret(ctx, b) else nil,
    "car": lambda ctx, lst: interpret(ctx, lst)[0],
    "cdr": lambda ctx, lst: interpret(ctx, lst)[1:],
}


def interpret(ctx, prog):
    while True:
        if isinstance(prog, str):
            return ctx[prog]
        if isinstance(prog, int):
            return prog
        cmd, *args = prog
        value = interpret(ctx, cmd)(ctx, *args)
        if not isinstance(value, DelayedInterpret):
            return value
        ctx, prog = value.ctx, value.prog


def run(code, flag=None):
    code = code.replace(" ", ",")
    code = code.replace("(", "[")
    code = code.replace(")", "]")
    return interpret(base_ctx | {"flag": flag}, yaml.safe_load(code))


assert run("(+ 1 2 3)") == 6
assert run("(- 5 7)") == -2
assert run("(+ (+ 1 2) 3)") == 6
assert run("(quote (+ 1 2))") == ["+", 1, 2]
assert run("(list 1 2)") == [1, 2]
assert run("(list 1 2 (list 3 4))") == [1, 2, [3, 4]]
assert run("nil") == nil
assert run("(if nil (list 1 2) (list 3 4))") == [3, 4]
assert run("(eq 5 (+ 2 3))") == True
assert run("(lt 2 3)") == True
assert run("(gt 2 3)") == nil
assert run("((lambda (arg) (+ arg 1)) 5)") == 6
assert run("(car (list 1 2 3))") == 1
assert run("(cdr (list 1 2 3))") == [2, 3]

run(input(), flag=list(os.environ["FLAG"].encode()))
