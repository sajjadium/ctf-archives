import os
import string
import secrets
from subprocess import Popen, PIPE

os.chdir(os.path.dirname(os.path.abspath(__file__)))

FLAG = os.getenv("FLAG", "srdnlen{fake_flag}")

MAYO_SCHEME = "MAYO-2"
ALPHABET = string.ascii_letters + string.digits

def main():
    choice = input("""Choose what to do
1. Get signature
2. Get flag

choice: """)

    if choice not in ["1", "2"]:
        print("Invalid choice")
        return

    if choice == "1":
        idx = input("Choose the index of the byte to edit: ")
        if not idx.isdigit() or int(idx) < 0x5a84 or int(idx) >= 0x687a:
            print("Invalid index")
            return

        idx = int(idx)

        idx2 = input("Choose which nibble to edit: ")
        if idx2 not in ["0", "1"]:
            print("Invalid choice")
            return

        idx2 = int(idx2)

        val = input("Choose the value to write: ")
        if not val.isdigit() or int(val) >= 256:
            print("Invalid value")
            return

        val = int(val)

        with open("chall", "rb") as f:
            chall_binary = f.read()

        chall_binary_patched = chall_binary[:idx] + bytes([(chall_binary[idx] & (0xf0 if idx2 else 0x0f)) | (val << (0 if idx2 else 4))]) + chall_binary[idx+1:]

        chall_patched_name = f"chall_patched_{secrets.token_hex(16)}"
        with open(chall_patched_name, "wb") as f:
            f.write(chall_binary_patched)

        os.system(f"chmod +x ./{chall_patched_name}")

        proc = Popen([f"./{chall_patched_name}", MAYO_SCHEME], stdout=PIPE)

        res = proc.wait()

        print(f"process terminated with code: {res}\noutput: {proc.stdout.read()}")

        os.system(f"rm ./{chall_patched_name}")
    else:
        target_message = "".join([secrets.choice(ALPHABET) for _ in range(32)])
        sig_hex = input(f"enter the signature for the message \"{target_message}\" (in hex): ")

        proc = Popen(["./check_solve", MAYO_SCHEME, target_message, sig_hex])

        res = proc.wait()

        if res == 0:
            print(f"Congratulations, here is your flag: {FLAG}")
        else:
            print("No flag for you")

if __name__ == "__main__":
    main()
