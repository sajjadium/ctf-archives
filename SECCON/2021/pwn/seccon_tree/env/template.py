from seccon_tree import Tree

# Debug utility
seccon_print = print
seccon_bytes = bytes
seccon_id = id
seccon_range = range
seccon_hex = hex
seccon_bytearray = bytearray
class seccon_util(object):
    def Print(self, *l):
        seccon_print(*l)
    def Bytes(self, o):
        return seccon_bytes(o)
    def Id(self, o):
        return seccon_id(o)
    def Range(self, *l):
        return seccon_range(*l)
    def Hex(self, o):
        return seccon_hex(o)
    def Bytearray(self, o):
        return seccon_bytearray(o)

dbg = seccon_util()

# Disallow everything
for key in dir(__builtins__):
    del __builtins__.__dict__[key]
del __builtins__


/** code **/
