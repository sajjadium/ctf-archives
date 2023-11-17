def encrypt(message):
    encrypted_message = ""
    for char in message:
        a = (ord(char) * 2) + 10
        b = (a ^ 42) + 5
        c = (b * 3) - 7
        encrypted_char = c ^ 23
        encrypted_message += chr(encrypted_char)
    return encrypted_message

flag = "INTIGRITI{REDACTED}"
encrypted_flag = encrypt(flag)

with open("flag.txt.enc", "w") as file:
    file.write(encrypted_flag)