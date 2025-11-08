import io
import contextlib

with open("flag.txt", 'rb') as f:
    FLAG = f.read()

def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {})
    except Exception:
        return None
    return buf.getvalue() or None

code = input("Enter your solution: ")

if len(code) > 15:
    print("Code too long")
    exit()

if not set(code) <= set("abcdefghijklmnopqrstuvwxyz "):
    print("Invalid characters")
    exit()

result = run(code)

if result is None:
    print("Error")
    exit()

if len(result) > 500:
    print(FLAG)
else:
    print("Output too short")
