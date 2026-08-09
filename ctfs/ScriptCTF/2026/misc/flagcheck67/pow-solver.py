import hashlib

prefix = "MJuFZ7F8ot4hVO5l"
target_bits = 22

nonce = 0

while True:
    s = prefix + str(nonce)
    h = hashlib.sha256(s.encode()).digest()

    if int.from_bytes(h, "big") >> (256 - target_bits) == 0:
        print("Solution:", nonce)
        print("Input:", s)
        print("SHA256:", h.hex())
        break

    nonce += 1
