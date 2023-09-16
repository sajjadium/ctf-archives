import sys
import re
import os
import subprocess
import tempfile

FLAG = os.environ["FLAG"]
assert re.fullmatch(r"SECCON{[_a-z0-9]+}", FLAG)
os.environ.pop("FLAG")

TEMPLATE = """
fn main() {
    {{YOUR_PROGRAM}}

    /* Steal me: {{FLAG}} */
}
""".strip()

print("""
🦀 Compile-Time Sandbox Escape 🦀

Input your program (the last line must start with __EOF__):
""".strip(), flush=True)

program = ""
while True:
    line = sys.stdin.readline()
    if line.startswith("__EOF__"):
        break
    program += line
if len(program) > 512:
    print("Your program is too long. Bye👋".strip())
    exit(1)

source = TEMPLATE.replace("{{FLAG}}", FLAG).replace("{{YOUR_PROGRAM}}", program)

with tempfile.NamedTemporaryFile(suffix=".rs") as file:
    file.write(source.encode())
    file.flush()

    try:
        proc = subprocess.run(
            ["rustc", file.name],
            cwd="/tmp",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2,
        )
        print(":)" if proc.returncode == 0 else ":(")
    except subprocess.TimeoutExpired:
        print("timeout")
