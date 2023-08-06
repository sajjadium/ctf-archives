from RestrictedPython import safe_globals
from RestrictedPython import utility_builtins
from RestrictedPython import compile_restricted
from RestrictedPython import Eval
from RestrictedPython import PrintCollector
from RestrictedPython import Guards
policy_globals = {**safe_globals, **utility_builtins}
del policy_globals['string'] # ok like who needs string.Formatter tho like i dont
policy_globals['random']._________top_secret_flag_in_here_omg______ = open("flag.txt").read()
cod = input(">>> ")
byte_code = compile_restricted(cod, filename="<string>", mode="eval")
print(eval(byte_code, policy_globals, None))
