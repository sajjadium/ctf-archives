import ast
import irs

dangerous = lambda s: any(d in s for d in ("__", "attr"))
dangerous_attr = lambda s: dangerous(s) or s in dir(dict)
dangerous_nodes = (ast.Starred, ast.GeneratorExp, ast.Match, ast.With, ast.AsyncWith, ast.keyword, ast.AugAssign)

print("Welcome to the IRS! Enter your code:")
c = ""
while l := input("> "): c += l + "\n"
root = ast.parse(c)
for node in ast.walk(root):
    for child in ast.iter_child_nodes(node):
        child.parent = node
if not any(type(n) in dangerous_nodes or
           type(n) is ast.Name and dangerous(n.id) or
           type(n) is ast.Attribute and dangerous_attr(n.attr) or
           type(n) is ast.Subscript and type(n.parent) is not ast.Delete or
           type(n) is ast.arguments and (n.kwarg or n.vararg)
           for n in ast.walk(root)):
    del __builtins__.__loader__
    del __builtins__.__import__
    del __builtins__.__spec__
    irs.audit()
    exec(c, {}, {})
