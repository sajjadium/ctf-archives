import ast

def safe_import():
  print("Why do you need imports to make tea?")

def safe_call():
  print("Why do you need function calls to make tea?")

class CoolDownTea(ast.NodeTransformer):
  def visit_Call(self, node: ast.Call) -> ast.AST:
    return ast.Call(func=ast.Name(id='safe_call', ctx=ast.Load()), args=[], keywords=[])
  
  def visit_Import(self, node: ast.AST) -> ast.AST:
    return ast.Expr(value=ast.Call(func=ast.Name(id='safe_import', ctx=ast.Load()), args=[], keywords=[]))
  
  def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST:
    return ast.Expr(value=ast.Call(func=ast.Name(id='safe_import', ctx=ast.Load()), args=[], keywords=[]))
  
  def visit_Assign(self, node: ast.Assign) -> ast.AST:
    return ast.Assign(targets=node.targets, value=ast.Constant(value=0))
  
  def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
    return ast.BinOp(left=ast.Constant(0), op=node.op, right=ast.Constant(0))
  
code = input('Nothing is quite like a cup of tea in the morning: ').splitlines()[0]

cup = ast.parse(code)
cup = CoolDownTea().visit(cup)
ast.fix_missing_locations(cup)

exec(compile(cup, '', 'exec'), {'__builtins__': {}}, {'safe_import': safe_import, 'safe_call': safe_call})