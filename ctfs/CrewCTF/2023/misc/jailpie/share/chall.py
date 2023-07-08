#!/usr/local/bin/python3
import base64
import types
import dis

def is_valid(code):
    whitelist = {
        'LOAD_CONST',
        'BINARY_OP',
        'COMPARE_OP',
        'POP_JUMP_BACKWARD_IF_TRUE',
        'RETURN_VALUE',
    }

    for instr in dis.Bytecode(code):
        if instr.opname not in whitelist:
            return False

        if 'JUMP' in instr.opname and not (0 <= instr.argval < len(code.co_code)):
            return False
    
    return True

if __name__ == '__main__':
    _print, _eval = print, eval
    # try:
    prog = bytes.fromhex(input('Program: '))
    code = types.CodeType(0, 0, 0, 0, 0, 0, prog, (0,), (), (), '', '', '', 0, b'', b'', (), ())
    assert is_valid(code)

    __builtins__.__dict__.clear()
    _print(_eval(code, {}))
    # except:
    #     _print('Nice try!')
