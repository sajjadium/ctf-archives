from Crypto.Cipher import AES as AES_BLOCK
import secrets
import random

AES_BLOCK_SIZE = 16
MODE_BLOCK_SIZE = AES_BLOCK_SIZE * 16

KEY = secrets.token_bytes(AES_BLOCK_SIZE)
AES = AES_BLOCK.new(KEY, AES_BLOCK.MODE_ECB)

import random
random.seed(KEY)

PERMUTATION = list(range(AES_BLOCK_SIZE))
random.shuffle(PERMUTATION)

def encrypt(inp):
    inp = inp.ljust(MODE_BLOCK_SIZE, b"\x00")
    
    assert len(inp) % MODE_BLOCK_SIZE == 0

    data = b""
    for block in range(0, len(inp), MODE_BLOCK_SIZE):
        for i in range(AES_BLOCK_SIZE):
            data += bytes(inp[block+j*AES_BLOCK_SIZE+PERMUTATION[i]] for j in range(MODE_BLOCK_SIZE // AES_BLOCK_SIZE))
    
    return AES.encrypt(data)

def decrypt(inp):
    assert len(inp) % MODE_BLOCK_SIZE == 0

    inp = AES.decrypt(inp)
    data = b""
    for block in range(0, len(inp), MODE_BLOCK_SIZE):
        for j in range(MODE_BLOCK_SIZE // AES_BLOCK_SIZE):
            for i in range(AES_BLOCK_SIZE):
                data += bytes([inp[block + PERMUTATION.index(i) * (MODE_BLOCK_SIZE // AES_BLOCK_SIZE) + j]])
  
    return data

import json

def make_echo(inp):
    data = json.dumps({"type": "echo", "msg": inp}).encode(errors="ignore")
    assert len(data) < 2**32
    return len(data).to_bytes(length=2, byteorder="little") + data

def run_command(inp):
    inp = decrypt(inp)
    length = int.from_bytes(inp[:2], byteorder="little")
    if length + 2 >= len(inp):
        return "Invalid command"
    
    # Show me what you got
    command = inp[2:length+2].decode("ascii", errors="replace")
    try:
        command = json.loads(command, strict=False)
    except Exception as e:
        return "Invalid command"

    if "type" not in command:
        return "No command type"

    match command["type"]:
        case "echo":
            return command.get("msg", "Hello world!")
        case "flag":
            with open("/flag", "r") as f:
                return f.read()
        case other:
            return f"Unknown command type {command['type']}..."

BANNER = "This is an echo service. This interface is protected by AES-BAD-256 technology."

MENU = """
1. Get an echo command
2. Run a command
3. Exit
"""

def main():
    print(BANNER)
    while True:
        print(MENU)
        command = input("> ")
        match command:
            case "1":
                print("Give me some text.\n")
                data = input("> ")
                print(encrypt(make_echo(data)).hex())
            case "2":
                print("Give me a command.\n")
                data = bytes.fromhex(input("(hex) > "))
                print(run_command(data))
            case other:
                print("Bye!")
                exit(0)
                

if __name__ == "__main__":
    main()
