import random

def generate_string(length):
    # This function generates a random string of the specified length
    byte_list = [(random.randint(0, 127) + 256)//2 for _ in range(length)]
    byte_string = bytes(byte_list)
    utf8_string = byte_string.decode('utf-8', errors='replace')
    return utf8_string

def xor_cipher(message, key):
    # This function performs XOR encryption on the message and key
    message_nums = [ord(c) for c in message]
    key_nums = [ord(c) for c in key]
    cipher_nums = [m ^ k for m, k in zip(message_nums, key_nums)]
    return ''.join(chr(i) for i in cipher_nums)

# Example usage
flag = "grodno{fake_flag}"
key = generate_string(len(flag))
print("key:", key)

if len(flag) > len(key):
    raise ValueError("The key length must not be less than the message length")
if len(flag) < len(key):
    key = key[:len(flag)]

encrypted_flag = xor_cipher(flag, key)
print("encrypted_flag:", encrypted_flag)
with open("encrypted_flag.txt", 'w', encoding='utf-8') as file:
    file.write(encrypted_flag)
