from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = open("key.txt", "rb").read().strip()
flag = pad(open("flag.txt", "rb").read(), 16)
cipher = AES.new(key, AES.MODE_ECB)
open("output.txt", "w+").write(cipher.encrypt(flag).hex())
