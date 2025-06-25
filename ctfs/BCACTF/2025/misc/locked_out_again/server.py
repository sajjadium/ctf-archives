#!/usr/bin/env python3


class DescriptorTrap:
    def __init__(self, name):
        self.name = name
        self.access_count = 0

    def __get__(self, obj, objtype=None):
        self.access_count += 1
        if self.access_count > 3:
            raise Exception(f"Too many accesses to {self.name}!")
        return lambda *args, **kwargs: None

    def __set__(self, obj, value):
        raise Exception(f"Cannot modify {self.name}!")


class MetaTrap(type):
    def __new__(cls, name, bases, namespace):
        for attr in ["print", "exec", "eval", "open", "input", "__import__"]:
            namespace[attr] = DescriptorTrap(attr)

        # Make all methods return None after 2 calls
        for key, value in namespace.items():
            if callable(value) and not key.startswith("__"):
                namespace[key] = DescriptorTrap(key)

        return super().__new__(cls, name, bases, namespace)

    def __getattribute__(cls, name):
        if name in ["__dict__", "__class__", "__bases__", "__mro__"]:
            raise Exception("No metaclass inspection allowed!")
        return super().__getattribute__(name)


class JailCell(metaclass=MetaTrap):
    # These will be trapped by the metaclass
    print = print
    exec = exec
    eval = eval
    open = open
    __import__ = __import__

    def escape_attempt(self):
        return "Nice try!"


# Create the jail environment
jail = JailCell()

# Block access to dangerous builtins
blocked_builtins = {
    "exec",
    "eval",
    "compile",
    "open",
    "__import__",
    "input",
    "breakpoint",
    "help",
    "exit",
    "quit",
    "copyright",
    "credits",
}

if hasattr(__builtins__, "__dict__"):
    builtin_dict = __builtins__.__dict__
else:
    builtin_dict = __builtins__

safe_builtins = {k: v for k, v in builtin_dict.items() if k not in blocked_builtins}


safe_builtins["print"] = lambda *args, **kwargs: None  # Neuter print
safe_builtins["open"] = lambda *args, **kwargs: None  # Neuter open

print("read the contents of ./flag.txt")
print("man i LOVE wjat.")

user_code = input("enter your escape code: ")

try:
    exec(user_code, {"__builtins__": safe_builtins, "jail": jail}, {})
except Exception as e:
    print("why are you failing me. come on.")
