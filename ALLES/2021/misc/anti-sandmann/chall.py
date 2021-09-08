import readline as __readline
import code as __code

class __Frozen(dict):
    def __init__(self, v):
        super().__init__(v)
    def __setitem__(self, k, v):
        exit(1)

__shell = __code.InteractiveConsole(filename="sandbox")
__locals = {}
__shell.runcode=lambda code: [exit(1) if any('"' in y or "'" in y or "#" in y or '__' in y for y in __shell.buffer) else exec(code, __Frozen({'__builtins__': __Frozen({})}), __locals), setattr(__shell, "filename", "sandbox")]
__shell.interact()