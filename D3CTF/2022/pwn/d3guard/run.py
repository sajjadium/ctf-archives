import os, subprocess
import random

def main():
    try:
        ret = subprocess.call([
            "qemu-system-x86_64",
            "-m", f"{256+random.randint(0, 512)}",
            "-drive", f"if=pflash,format=raw,file=OVMF.fd",
            "-drive", "file=fat:rw:contents,format=raw",
            "-net", "none",
            "-monitor", "/dev/null",
            "-nographic"
        ], stderr=subprocess.DEVNULL)
        print("Return:", ret)
    except:
        print("Error!")
    finally:
        print("Done.")

if __name__ == "__main__":
    main()
