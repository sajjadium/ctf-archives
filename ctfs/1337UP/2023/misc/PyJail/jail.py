import ast
import unicodedata

blacklist = "0123456789[]\"\'._"
check = lambda x: any(w in blacklist for w in x)

def normalize_code(code):
    return unicodedata.normalize('NFKC', code)

def execute_code(code):
    try:
        normalized_code = normalize_code(code)
        parsed = ast.parse(code)
        for node in ast.walk(parsed):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ("os","system","eval","exec","input","open"):
                        return "Access denied!"
            elif isinstance(node, ast.Import):
                return "No imports for you!"
        if check(code):
            return "Hey, no hacking!"
        else:
            return exec(normalized_code, {}, {})
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    while True:
        user_code = input(">> ")
        if user_code.lower() == 'quit':
            break
        result = execute_code(user_code)
        print("Result:", result)