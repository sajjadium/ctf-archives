#!/usr/bin/env python3

import base64
import sys
import subprocess

def main():    
    elf_path = "/tmp/elf"
    try:
        elf_data = base64.b64decode(input("Please provide base64 encoded ELF: "))
        with open(elf_path, "wb") as f:
            f.write(elf_data)
        subprocess.run(["/dwarf", elf_path])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
