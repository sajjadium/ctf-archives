#!/usr/bin/env python3
# Thanks CSAW2023 for the inspiration
import ast
import sys

BANNED = {
    #def not
    ast.Import,
    ast.ImportFrom,
    ast.With,
    ast.alias,
    ast.Attribute,
    ast.Constant,

    #should be fine?
    ast.Subscript,
    ast.Assign,
    ast.AnnAssign,
    ast.AugAssign,
    ast.For,
    ast.Try,
    ast.ExceptHandler,
    ast.With,
    ast.withitem,
    ast.FunctionDef,
    ast.Lambda,
    ast.ClassDef,


    #prob overkill but should be fine
    ast.If,
    ast.And,
    ast.comprehension,
    ast.In,
    ast.Await,
    ast.Global,
    ast.Gt,
    ast.ListComp,
    ast.Slice,
    ast.Return,
    ast.List,
    ast.Dict,
    ast.Lt,
    ast.AsyncFunctionDef,
    ast.Eq,
    ast.keyword,
    ast.Mult,
    ast.arguments,
    ast.FormattedValue,
    ast.Not,
    ast.BoolOp,
    ast.Or,
    ast.Compare,
    ast.GtE,
    ast.ImportFrom,
    ast.Tuple,
    ast.NotEq,
    ast.IfExp,
    ast.alias,
    ast.arg,
    ast.JoinedStr,

    # Patch some more >:)
    ast.Match, 
    ast.Del,
    ast.Starred,
    ast.Is,
    ast.NamedExpr,
}

def hook(event, args):
    if not hook.exec and 'exec' in event:
        hook.exec = True
        return

    strr = event + " ".join(f"{x}" for x in args)
    strr = strr.lower()
    if any(i in strr for i in [
        'exec',
        'print',
        'import', 
        'system', 
        'flag', 
        'spawn',
        'fork', 
        'open', 
        'subprocess', 
        'sys',
        'ast', 
        'os',
        'audit',
        'hook'
        'compile',
        '__new__',
        'frame']):
        print("BONK audit!", event + " " + " ".join(f"{x}" for x in args))
        exit()

    # print("audit!", event + " " + " ".join(f"{x}" for x in args))
    

hook.exec = False

def banner():
    print("Hello world! Please input your program here: ")

    code = input()

    for n in ast.walk(ast.parse(code)):
        if type(n) in BANNED:
            print("BAD CODE! BONK!: " + str(type(n)))
            exit()
    
    return code

code = banner()
code = compile(code, "<code>", "exec")

safer_builtins = __builtins__.__dict__.copy()
banned_builtins = [
    'exec',
    'eval',
    'compile',
    'type',
    'globals',
    'dir',
    'callable',
    'type',
    'all',
    'any',
    'int',
    'input',
    'breakpoint',
    'print',
    'quit',
    'exit',
    'copyright',
    'credits',
    'license',
    'help',
]
for banned in banned_builtins:
    safer_builtins.pop(banned, None)

# safer 
sys.addaudithook(hook)

exec(code, {"__builtins__": safer_builtins})


