from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secret import flag

KEY_LEN = 2
BS = 16
key = pad(open("/dev/urandom","rb").read(KEY_LEN), BS)
iv =  open("/dev/urandom","rb").read(BS)

cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(flag, 16))

print(f"iv = {iv.hex()}")
print(f"ct = {ct.hex()}")

# Output:
# iv = 1df49bc50bc2432bd336b4609f2104f7
# ct = a40c6502436e3a21dd63c1553e4816967a75dfc0c7b90328f00af93f0094ed62