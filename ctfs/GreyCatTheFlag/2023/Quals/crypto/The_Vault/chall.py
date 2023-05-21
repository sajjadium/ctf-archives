from hashlib import sha256 
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes 
from math import log10 

FLAG = "grey{fake_flag}"

n = pow(10, 128)
def check_keys(a, b):
    if a % 10 == 0:
        return False  

    # Check if pow(a, b) > n
    if b * log10(a) > 128:
        return True 
    return False 

def encryption(key, plaintext):
    iv = "Greyhats".encode()
    cipher = AES.new(key, AES.MODE_CTR, nonce = iv)
    return cipher.encrypt(plaintext)

print("Welcome back, NUS Dean. Please type in the authentication codes to open the vault! \n")

a = int(input("Enter the first code: "))
b = int(input("Enter the second code: "))

if not check_keys(a, b):
    print("Nice try thief! The security are on the way.")
    exit(0)

print("Performing thief checks...\n")
thief_check = get_random_bytes(16)

# Highly secure double encryption checking system. The thieves stand no chance!
x = pow(a, b, n)
first_key = sha256(long_to_bytes(x)).digest()
second_key = sha256(long_to_bytes(pow(x, 10, n))).digest()

if thief_check == encryption(first_key, encryption(second_key, thief_check)):
    print("Vault is opened.")
    print(FLAG)
else:
    print("Stealing attempts detected! Initializing lockdown")