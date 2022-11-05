import os, subprocess
import random

def main():
    try:
        os.system("rm -f OVMF.fd")
        os.system("cp OVMF.fd.bak OVMF.fd")
        ret = subprocess.call([
            "qemu-system-x86_64",
            "-m", str(256+random.randint(0, 512)),
            "-drive", "if=pflash,format=raw,file=OVMF.fd",
            "-drive", "file=fat:rw:contents,format=raw",
            "-net", "none",
            "-monitor", "/dev/null",
            "-nographic"
        ])
        print("Return:", ret)
    except Exception as e:
        print(e)
        print("Error!")
    finally:
        print("Done.")

if __name__ == "__main__":
    main()