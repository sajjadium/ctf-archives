import sys
from algorithm import encrypt

def encrypt_file(input_file: str, output_file: str):
    with open(input_file, 'rb') as infile:
        data = infile.read()

    encrypted_data = encrypt(data)

    with open(output_file, 'wb') as outfile:
        outfile.write(encrypted_data)

    print(f"File {input_file} has been encrypted and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python encrypt_file.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        encrypt_file(input_file, output_file)
