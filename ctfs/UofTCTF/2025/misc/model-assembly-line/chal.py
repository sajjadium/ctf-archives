import ast

class CodeValidator:
    FUNCTION_NAME = "YOUR_MODEL"
    UNSAFE_TYPES = (
        ast.Import, ast.ImportFrom, ast.Attribute, 
        ast.Try, ast.TryStar, ast.Assert, ast.Global,
        ast.Nonlocal, ast.Delete, ast.Call,
        ast.FunctionDef, ast.AsyncFunctionDef,
        ast.ClassDef, ast.Lambda
    )

    @staticmethod
    def read_input(end_marker="$$END$$"):
        print("Enter your model code below. End with '$$END$$' on a new line:")
        try:
            code_lines = []
            while True:
                line = input()
                if line.strip() == end_marker:
                    break
                code_lines.append(line + "\n")
            return "".join(code_lines)
        except KeyboardInterrupt:
            raise ValueError("Input reading interrupted")

    @staticmethod
    def validate_function_def(node):
        if not isinstance(node, ast.FunctionDef):
            return False, "Top level node must be a function"
            
        if node.name != CodeValidator.FUNCTION_NAME:
            return False, f"Function must be named {CodeValidator.FUNCTION_NAME}"

        if node.decorator_list:
            return False, "Function cannot have decorators"

        args = node.args
        if any([
            args.posonlyargs,
            args.vararg,
            args.kwarg,
            args.defaults,
            args.kw_defaults,
            args.kwonlyargs
        ]):
            return False, "Function has invalid argument structure"

        return True, "Function definition valid"

class UnsafeNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.unsafe = False
        self.unsafe_nodes = []
        self.is_top_level = True

    def visit_FunctionDef(self, node):
        if self.is_top_level:
            self.is_top_level = False
            
            self.visit(node.args)
            if node.returns:
                self.visit(node.returns)
            for stmt in node.body:
                self.visit(stmt)
            if node.type_comment:
                self.visit(ast.parse(node.type_comment))
            if hasattr(node, 'type_params'):
                for param in node.type_params:
                    self.visit(param)
        else:
            # Nested functions are not allowed (TODO: We've gotten some complaints that you need these to write a valid model. Maybe we should allow them in the beta version?)
            self.unsafe = True
            self.unsafe_nodes.append('FunctionDef')
        super().generic_visit(node)

    def generic_visit(self, node):
        if isinstance(node, CodeValidator.UNSAFE_TYPES) and not isinstance(node, ast.FunctionDef):
            self.unsafe = True
            self.unsafe_nodes.append(type(node).__name__)
        super().generic_visit(node)

def main():
    validator = CodeValidator()
    
    try:
        code = validator.read_input()
        if not code.strip():
            print("Error: Empty input")
            return

        tree = ast.parse(code)

        if len(tree.body) != 1:
            print("Error: Code must contain exactly one function definition at the top level, and nothing else")
            return
            
        is_valid, message = validator.validate_function_def(tree.body[0])
        if not is_valid:
            print(f"Error: {message}")
            return
        
        visitor = UnsafeNodeVisitor()
        visitor.visit(tree)
        if visitor.unsafe:
            print(f"Error: Unsafe nodes found: {', '.join(visitor.unsafe_nodes)}")
            return
        
        user_code = ast.unparse(tree.body[0])
        
        with open('template', 'r', encoding='utf-8') as f:
            template = f.read()
        
        filled_template = template.replace("{{YOUR_MODEL_CODE}}", user_code)

        try:
            exec_builtins = {'__builtins__': __builtins__}
            exec(filled_template, exec_builtins, exec_builtins)
        except:
            print("Huh, something went wrong. Does this thing even work properly?")
        
    except SyntaxError as e:
        print(f"Syntax error: {e}")
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()