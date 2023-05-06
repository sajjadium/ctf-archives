def encrypt(message, key):
    encrypted = ""
    for i in range(len(message)):
        encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted.encode("utf-8").hex()

message = #//////ERROR ERROR ERROR
key = #/////// ERROR OERROR ERROR ERROR
encrypted = encrypt(message,key)