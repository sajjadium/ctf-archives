import os
import secrets
import hashlib

# 2^64 = a lot of hashes, gpu go brr
FLAG_DIFFICULTY = 64

def main():
    for difficulty in range(1, FLAG_DIFFICULTY):
        print("You are on: Level", difficulty, "/", FLAG_DIFFICULTY)
        print("Please complete this Proof of Work to advance to the next level")
        print()

        power = ((1 << difficulty) - 1).to_bytes(32, 'big')
        request = secrets.token_bytes(2)
        print("sha256(", request.hex(), "|| nonce ) &", power.hex(), "== 0")
        nonce = bytes.fromhex(input("nonce = "))
        print()

        hash = hashlib.sha256(request + nonce).digest()
        if not all(a & b == 0 for a, b in zip(hash, power)):
            print("Incorrect PoW")
            return
        print("Correct")

    print("Congrats!")
    print(os.environ["FLAG"])

if __name__ == "__main__":
    main()
