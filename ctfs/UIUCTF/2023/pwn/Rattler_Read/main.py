from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import Guards
from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins
from RestrictedPython.PrintCollector import PrintCollector

def exec_poisonous(code):
    """Makes sure your code is safe to run"""

    def no_import(name, *args, **kwargs):
        raise ImportError("Don't ask another snake for help!")
    code += "\nresults = printed"
    byte_code = compile_restricted(
        code,
        filename="<string>",
        mode="exec",
    )
    policy_globals = {**safe_globals, **utility_builtins}
    policy_globals['__builtins__']['__metaclass__'] = type
    policy_globals['__builtins__']['__name__'] = type
    policy_globals['__builtins__']['__import__'] = no_import
    policy_globals['_getattr_'] = Guards.safer_getattr
    policy_globals['_getiter_'] = Eval.default_guarded_getiter
    policy_globals['_getitem_'] = Eval.default_guarded_getitem
    policy_globals['_write_'] = Guards.full_write_guard
    policy_globals['_print_'] = PrintCollector
    policy_globals['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence
    policy_globals['_unpack_sequence_'] = Guards.guarded_unpack_sequence
    policy_globals['enumerate'] = enumerate
    exec(byte_code, policy_globals, None)
    return policy_globals["results"]

if __name__ == '__main__':
    print("Well, well well. Let's see just how poisonous you are..")
    print(exec_poisonous(input('> ')))

