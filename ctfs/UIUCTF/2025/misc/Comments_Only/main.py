#!/usr/bin/env python3
import tempfile
import subprocess
import os

comment = input("> ").replace("\n", "").replace("\r", "")

code = f"""print("hello world!")
# This is a comment. Here's another:
# {comment}
print("Thanks for playing!")"""

with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
    f.write(code)
    temp_filename = f.name

try:
    result = subprocess.run(
        ["python3", temp_filename], capture_output=True, text=True, timeout=5
    )

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

except subprocess.TimeoutExpired:
    print("Timeout")
finally:
    os.unlink(temp_filename)
