import os
import base64
import random
import string
import tempfile
import subprocess

def main():

    flag = open("flag.txt", "r").read().rstrip()
    assert len(flag) == 42

    b64_data = input("Enter your base64-encoded rule file: ")

    try:
        rule_data = base64.b64decode(b64_data)
    except Exception:
        print(f"[ERROR] Failed to decode base64")
        exit()

    if len(rule_data) > 128:
        exit()

    uid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".rule") as rule_file:
        rule_file.write(rule_data)
        rule_path = rule_file.name

    try:
        # Most of these options are just to make hashcat more resource-friendly on remote
        process = subprocess.Popen(
            [
                "hashcat", "-D", "1","-d", "1", f"--session={uid}", "-m"
                "1400", "-w", "1", "-r", rule_path, "--potfile-disable",
                "hash.txt", "flag.txt",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=os.environ
        )

        for line in process.stdout:
            if 'Status' in line.decode():
                print(line.decode())
                break

        process.stdout.close()
        process.wait()

    except Exception:
        print(f'[ERROR] Failed to run hashcat')
    finally:
        os.remove(rule_path)

if __name__ == "__main__":
    main()
