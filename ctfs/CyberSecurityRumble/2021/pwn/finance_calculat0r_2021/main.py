import ast
import hashlib
import base64
from ecdsa import BadSignatureError, SigningKey

SIGNING_KEY = SigningKey.generate(hashfunc=hashlib.md5)


WHITELIST_NODES = [
    ast.Expression,
    ast.Expr,
    ast.Num,
    ast.Name,
    ast.Constant,
    ast.Load,
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Module,
    ast.Mult,
    ast.Div,
    ast.Assign,
    ast.Store
]

WHITELIST_FUNCTIONS = [
    "print"
]


EXAMPLE_PROG = """a = 31337
b = 9999
c = a * b + 777
print(c)"""

class WhitelistNodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        if type(node) not in WHITELIST_NODES:
            raise ValueError("Node type '{}' NOT allowed!".format(type(node)))
        super(WhitelistNodeVisitor, self).generic_visit(node)

    def visit_Call(self, call):
        if call.func.id not in WHITELIST_FUNCTIONS:
            raise ValueError("Forbidden function '{}'!".format(call.func.id))


def check_code_security(code):
    # Decode for parser
    s = code.decode(errors="ignore")
    tree = ast.parse(s, mode='exec')
    cnv = WhitelistNodeVisitor()
    cnv.visit(tree)


def run_code(code):
    # Decode for parser
    code = code.decode(errors="ignore")
    code = compile(code, "", "exec")
    eval(code)


def sign(data):
    return SIGNING_KEY.sign(data)


def verify_signature(signature, data):
    print("Supplied Sig:", signature)
    try:
        SIGNING_KEY.verifying_key.verify(signature, data)
        return True
    except BadSignatureError:
        return False


def read_prog():
    print("~" * 52)
    print("To avoid line breaks submit your programs in base64.")

    prog_b64 = input("Program> ")
    prog = base64.b64decode(prog_b64)
    
    return prog


def read_signed_prog():
    print("~" * 52)
    print("To avoid line breaks submit your programs in base64.")

    prog_inp = input("Signed Program> ")
    signature, prog_b64 = prog_inp.split(":", 1)
    prog = base64.b64decode(prog_b64)
    print("prog:", prog)
    signature = bytes.fromhex(signature)
    
    return signature, prog


def verify_and_sign():
    code = read_prog()

    # If program is unknown, check for safety
    try:
        check_code_security(code)
    except ValueError as ex:
        print("The program uses invalid code! Nice try hacker!")
        raise

    print("Your signed program:")
    print(sign(code).hex() + ":" + base64.b64encode(code).decode())


def run_signed_program():
    signature, code = read_signed_prog()

    if not verify_signature(signature, code):
        print("Invalid signature! This incident will be reported!")
        raise ValueError()

    print("*" * 20)
    print("Your Output:")

    run_code(code)

    print("*" * 20, end="\n\n")


def menu():
    print("~" * 52)
    print("What would you like to do?")
    print("  1. Verify and Sign Program")
    print("  2. Run Signed Program")
    print("~" * 52)
    choice = input("Choice >")

    try:
        choice = int(choice)
        if choice == 1:
            verify_and_sign()
        elif choice == 2:
            run_signed_program()
        else:
            raise ValueError()
    except (KeyError, ValueError):
        print("Invalid Input!")


def main():
    print("~" * 52)
    print("Welcome to finance calculat0r 2021")
    print("The number 1 app for heavy number processing!")
    print("Example batch program:")
    print(EXAMPLE_PROG)
    print("~" * 52)
    
    for _ in range(10):
        menu()
    
    print("You've already run 10 programs! For more please buy our enterprise edition!")

main()
