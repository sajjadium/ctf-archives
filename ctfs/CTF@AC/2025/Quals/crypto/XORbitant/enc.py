import os

def xor(input_path: str, output_path: str):
    key = os.getenv("FLAG","CTF{example_flag}") 

    key_bytes = key.encode("utf-8")
    key_len = len(key_bytes)

    with open(input_path, "rb") as infile, open(output_path, "wb") as outfile:
        chunk_size = 4096
        i = 0
        while chunk := infile.read(chunk_size):
            xored = bytes([b ^ key_bytes[(i + j) % key_len] for j, b in enumerate(chunk)])
            outfile.write(xored)
            i += len(chunk)

xor("plaintext.txt","out.bin")