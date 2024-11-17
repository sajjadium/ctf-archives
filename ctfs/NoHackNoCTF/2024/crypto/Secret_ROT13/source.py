def encrypt(text, key):
    encrypted_text = ""
    for i, char in enumerate(text):
        offset = ((i + 1 + key) * (i + 1)) % 26 
        if 'A' <= char <= 'Z':
            new_char = chr((ord(char) - ord('A') + offset) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            new_char = chr((ord(char) - ord('a') + offset) % 26 + ord('a'))
        else:
            new_char = char 
        encrypted_text += new_char
    return encrypted_text

# 測試範例
key = 7
plaintext = "NHNC{TEST}"
ciphertext = encrypt(plaintext, key)
print("加密後的密文:", ciphertext)
