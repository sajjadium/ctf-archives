#!/usr/local/bin/python
import subprocess
import tempfile

if __name__ == '__main__':
    print("Enter your code (End with '__EOF__\\n')")
    code = ''
    while True:
        line = input()
        if line == '__EOF__':
            break
        code += line + "\n"

    with tempfile.NamedTemporaryFile('w') as f:
        f.write(code)
        f.flush()

        p = subprocess.Popen(["./toy", f.name],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result = p.communicate()
        print(result[0].decode())
        print("[+] Done.")
