from pwn import *
FLAG = os.environ.get("FLAG", "FMCTF{F4K3_FL49}").encode()
key = os.urandom(7)
encryptedFlag = xor(FLAG, key).hex()
print(f"encryptedFlag = {encryptedFlag}")
# encryptedFlag = a850d725cb56b0de4fcb40de72a4df56a72ec06cafa75ecb41f51c95