from types import CodeType, FunctionType
from opcode import opname, opmap
import dis
import sys

BAD_ATTRS = ["func_globals", "f_globals", "f_locals", "f_builtins", "gi_code", "co_code", "gi_frame"]

BAD_OPCODES = {opmap[opname] for opname in
               ['STORE_ATTR', 'DELETE_ATTR', 'STORE_GLOBAL', 'DELETE_GLOBAL', 'DELETE_SUBSCR', 'IMPORT_STAR',
                'IMPORT_NAME', 'IMPORT_FROM']}

BUILTINS = {
    'enumerate': enumerate,
    'int': int,
    'zip': zip,
    'True': True,
    'filter': filter,
    'list': list,
    'max': max,
    'float': float,
    'divmod': divmod,
    'unicode': str,
    'min': min,
    'range': range,
    'sum': sum,
    'abs': abs,
    'sorted': sorted,
    'repr': repr,
    'isinstance': isinstance,
    'bool': bool,
    'set': set,
    'Exception': Exception,
    'tuple': tuple,
    'chr': chr,
    'function': FunctionType,
    'ord': ord,
    'None': None,
    'round': round,
    'map': map,
    'len': len,
    'bytes': bytes,
    'str': str,
    'all': all,
    'xrange': range,
    'False': False,
    'any': any,
    'dict': dict,
}


def check_co(co):
    for to_check in co.co_names + co.co_consts:
        if type(to_check) is str and ("__" in to_check or to_check in BAD_ATTRS):
            raise Exception(f"Bad attr: {to_check}")

    opcodes = {instruction.opcode for instruction in dis.get_instructions(co)}
    if opcodes.intersection(BAD_OPCODES):
        raise Exception(f"Bad opcode(s): {', '.join(opname[opcode] for opcode in opcodes.intersection(BAD_OPCODES))}")

    for const in co.co_consts:
        if isinstance(const, CodeType):
            check_co(const)


def safest_eval(expr):
    co = compile(expr, "", "exec")
    check_co(co)
    eval_globals =  {"__builtins__": dict(BUILTINS)}
    eval(co, eval_globals)
    return eval_globals


def palindrome_challenge(user_code):
    challenge_code = f"""
{user_code}

solved = False
if isinstance(is_palindrome, function):
    challenges = [["ooffoo", "murderforajarofredrum", "palindrome", ""], [True, True, False, True]]
    solved = list(map(is_palindrome, challenges[0])) == challenges[1]
"""

    try:
        eval_globals = safest_eval(challenge_code)
        if eval_globals["solved"] is True:
            print("Solved")
        else:
            print("Not Solved")
    except SyntaxError:
        print("SyntaxError")
    except Exception:
        print("Exception")


if __name__ == "__main__":
    palindrome_challenge(sys.argv[1])