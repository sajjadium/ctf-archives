from capstone import *
import subprocess
import tempfile
import signal


MAX_SHELLCODE_LEN = 250

md = Cs(CS_ARCH_X86, CS_MODE_64)


def handler(signum, frame):
    raise OSError("Wakeup")


def verify_shellcode(shellcode):
    # bypassing this filter is not intended
    # however if you come up with a bypass feel free to use it
    syscall_count = 0
    for i in md.disasm(shellcode, 0x0):
        if i.mnemonic != "mov" and i.mnemonic != "syscall":
            print("Invalid instruction: ")
            print(f"{hex(i.address)}:\t{i.mnemonic}\t{i.op_str}")
            exit(0)
        elif i.mnemonic == "syscall":
            if syscall_count < 2:
                syscall_count += 1
            else:
                print(f"Syscall limit reached @ {hex(i.address)}")
                exit(0)
        else:
            pass

def execute(shellcode):
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(shellcode)
        tmp.seek(0)
        try:
            print(subprocess.check_output(f"./shellcode_executor {tmp.name}", shell=True))
        except Exception as e:
            print(e)
            
def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60)
    print(f"Please provide the shellcode in hex format ({MAX_SHELLCODE_LEN} bytes at most)")
    shellcode_hex = input("> ")[:MAX_SHELLCODE_LEN].strip().encode().lower()
    
    try:
        shellcode_hex = bytes(list(filter(lambda c: chr(c) in "0123456789abcdef", shellcode_hex)))
        shellcode = bytes.fromhex(shellcode_hex.decode())
        verify_shellcode(shellcode)

        # exit properly
        shellcode += b"\xb8\x3c\x00\x00\x00\x0f\x05"  # mov eax, 0x3c; syscall;
        execute(shellcode)
    except:
        print("Invalid input")


if __name__ == "__main__":
    main()
