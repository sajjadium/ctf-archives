from json import JSONDecodeError, loads, dumps
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

with open("flag") as f:
    flag = f.readline()

key = get_random_bytes(16)


def encrypt(plaintext: bytes) -> (bytes, bytes):
    iv = get_random_bytes(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    print("IV:", hexlify(iv).decode())
    return iv, aes.encrypt(plaintext)


def decrypt(ciphertext: bytes, iv: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(ciphertext)


def create_command(message: str) -> (str, str):
    payload = {"from": "guest", "act": "echo", "msg": message}
    payload = dumps(payload).encode()
    while len(payload) % 16 != 0:
        payload += b'\x00'
    iv, payload = encrypt(payload)
    return hexlify(iv).decode('utf-8'), hexlify(payload).decode('utf-8')


def run_command(iv: bytes, command: str):
    try:
        iv = unhexlify(iv)
        command = unhexlify(command)
        command = decrypt(command, iv)

        while command.endswith(b'\x00') and len(command) > 0:
            command = command[:-1]
    except:
        print("Failed to decrypt")
        return

    try:
        command = command.decode()
        command = loads(command)
    except UnicodeDecodeError:
        print(f"Failed to decode UTF-8: {hexlify(command).decode('UTF-8')}")
        return
    except JSONDecodeError:
        print(f"Failed to decode JSON: {command}")
        return

    match command["act"]:
        case "echo":
            msg = command['msg']
            print(f"You received the following message: {msg}")
        case "flag":
            if command["from"] == "admin":
                print(f"Congratulations! The flag is: {flag}")
            else:
                print("You don't have permissions to perform this action")
        case action:
            print(f"Invalid action {action}")


def show_prompt():
    print("-" * 75)
    print("1. Create command")
    print("2. Run command")
    print("3. Exit")
    print("-" * 75)

    try:
        sel = input("> ")
        sel = int(sel)

        match sel:
            case 1:
                msg = input("Please enter your message: ")
                iv, command = create_command(msg)
                print(f"IV: {iv}")
                print(f"Command: {command}")
            case 2:
                iv = input("IV: ")
                command = input("Command: ")
                run_command(iv, command)
            case 3:
                exit(0)
            case _:
                print("Invalid selection")
                return
    except ValueError:
        print("Invalid selection")
    except:
        print("Unknown error")


if __name__ == "__main__":
    while True:
        show_prompt()
