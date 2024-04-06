import random

# File to encrypt
file_name = input("Please input the filename: ")

# Choose whether to encrypt or decrypt the file
choice = input("Enter 'encrypt' or 'decrypt' to preform the respective operation on the selected file: ")

# Open the file
f = open(file_name, mode="rb")

# Read the file
data = f.read()

if choice == "encrypt":
    # Generate random numbers for the LCG
    seed = random.randint(1, 256)
    a = random.randint(1, 256)
    c = random.randint(1, 256)
    modulus = random.randint(1, 256)

    print(f"Seed: {seed}")
    print(f"A: {a}")
    print(f"C: {c}")
    print(f"Modulus: {modulus}")

    # Pad the file out with some filler bytes to obscure it's size
    arr = bytearray(data)
    arr += bytearray([0x41] * 1000)

    save = bytearray()

    # Encrypt the files contents with the LCG
    for i in arr:
        seed = (a * seed + c) % modulus
        save.append(i ^ seed)

    f.close()

    # Write the encrypted file back to the disk
    with open(f"{file_name}.enc", "wb") as binary_file:
        binary_file.write(save)

elif choice == "decrypt":
    seed = int(input("Seed: "))
    a = int(input("A: "))
    c = int(input("C: "))
    modulus = int(input("Modulus: "))

    # Remove the padding bytes
    arr = bytearray(data[:len(data)-1000])

    save = bytearray()

    # Decrypt the files contents with the LCG
    for i in arr:
        seed = (a * seed + c) % modulus
        save.append(i ^ seed)

        # Write the encrypted file back to the disk
        with open(f"{file_name}.dec", "wb") as binary_file:
            binary_file.write(save)


