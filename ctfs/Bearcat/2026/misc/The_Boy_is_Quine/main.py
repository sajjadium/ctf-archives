#!/usr/local/bin/python3 -u
import subprocess
from os import remove
from uuid import uuid4


def is_quine(code):
    filename = f"/tmp/{uuid4()}.py"
    try:
        with open(filename, "w") as f:
            f.write(code)

        result = subprocess.run(
            ["sudo", "-u", "quine", "/usr/local/bin/python3", filename],
            capture_output=True,
            text=True,
            timeout=5,
        )
        print(result.stderr, result.stdout)
        if result.stderr:
            remove(filename)
            return False
    except:
        remove(filename)
        return False
    remove(filename)
    return code == result.stdout


def main():
    print("Give me a quine")
    code = input("> ")
    if is_quine(code):
        print("That will do just fine.")
        exec(code)
    else:
        print("That was out of line!")


if __name__ == "__main__":
    main()
