import hashlib

stored_data = {}

def generate_keystream(i):
    return (i * 3404970675 + 3553295105) % (2 ** 32)

def upload_file():
    print("Choose a name for your file")
    name = input()
    if name in stored_data:
        print("There is already a file with that name")
        return
    print("Remember that your privacy is our top priority and all stored files are encrypted.")
    print("Choose a password")
    password = input()
    m = hashlib.shake_128()
    m.update(password.encode())
    keystream = int.from_bytes(m.digest(4), byteorder="big")
    print("Now upload the contents of your file in hexadecimal")
    contents = input()
    b = bytearray(bytes.fromhex(contents))
    for i in range(0, len(b), 4):
        key = keystream.to_bytes(4, byteorder="big")
        b[i + 0] ^= key[0]
        if i + 1 >= len(b):
            continue
        b[i + 1] ^= key[1]
        if i + 2 >= len(b):
            continue
        b[i + 2] ^= key[2]
        if i + 3 >= len(b):
            continue
        b[i + 3] ^= key[3]
        keystream = generate_keystream(keystream)
    stored_data[name] = b
    print("Your file has been uploaded and encrypted")


def view_files():
    print("Available files:")
    for i in stored_data.keys():
        print(i)
    print("Choose a file to get")
    name = input()
    if name not in stored_data:
        print("That file is not available")
        return
    print(stored_data[name].hex())

def main():
    print("Welcome to Augury")
    print("The best place for secure storage!")
    while True: 
        print("Please select an option:")
        print("1. Upload File")
        print("2. View Files")
        print("3. Exit")
        choice = input()
        match choice:
            case "1":
                upload_file()
            case "2":
                view_files()
            case "3":
                exit()

main()
