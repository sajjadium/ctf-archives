import os

flag = b"XXXXXX"
key = os.urandom(8)

cipher_text = b""

for i in range(len(flag)):
    cipher_text += bytes([flag[i] ^ key[i % 8]])


print(cipher_text.hex())


# flag 763d32726973a23f79373473616ba86a60300e677634f734482a626f6e5ff22e636a327c2f5ff228240123242e6caa23483d6127765fff6d743a61212f38bb