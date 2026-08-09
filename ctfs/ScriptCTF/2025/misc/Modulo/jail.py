import ast
print("Welcome to the jail! You're never gonna escape!")
payload = input("Enter payload: ") # No uppercase needed
blacklist = list("abdefghijklmnopqrstuvwxyz1234567890\\;._")
for i in payload:
    assert ord(i) >= 32
    assert ord(i) <= 127
    assert (payload.count('>') + payload.count('<')) <= 1
    assert payload.count('=') <= 1
    assert i not in blacklist

tree = ast.parse(payload)
for node in ast.walk(tree):
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ast.Mod): # Modulo because why not?
            raise ValueError("I don't like math :(")
exec(payload,{'__builtins__':{},'c':getattr}) # This is enough right?
print('Bye!')