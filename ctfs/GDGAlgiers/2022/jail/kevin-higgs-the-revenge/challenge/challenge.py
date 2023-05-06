#!/usr/bin/env python3

import pickle
import pickletools
import io
import sys

BLACKLIST_OPCODES = {
    "BUILD",
    "SETITEM",
    "SETITEMS",
    "DICT",
    "EMPTY_DICT",
    "INST",
    "OBJ",
    "NEWOBJ",
    "EXT1",
    "EXT2",
    "EXT4",
    "EMPTY_SET",
    "ADDITEMS",
    "FROZENSET",
    "NEWOBJ_EX",
    "FRAME",
    "BYTEARRAY8",
    "NEXT_BUFFER",
    "READONLY_BUFFER",
}

module = type(__builtins__)
empty = module("empty")
sys.modules["empty"] = empty


class MyUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "empty" and name.count(".") <= 1 and "setattr" not in name and "setitem" not in name:
            return super().find_class(module, name)
        else:
            raise pickle.UnpicklingError("No :(")


def check(data):
    return (
        all(
            opcode.name not in BLACKLIST_OPCODES
            for opcode, _, _ in pickletools.genops(data)
        )
        and len(data) <= 400
    )


if __name__ == "__main__":
    data = bytes.fromhex(input("Enter your hex-encoded pickle data: "))
    if check(data):
        result = MyUnpickler(io.BytesIO(data)).load()
        print(f"Result: {result}")
    else:
        print("Check failed :(")
