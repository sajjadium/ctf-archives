from Crypto.Util.number import *

p = getPrime(1024)
q = getPrime(1024)
r = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

print("Welcome to the enc-shop!")
print("What can I encrypt for you today?")


for _ in range(3):
    message = input("Enter text to encrypt: ")
    m = bytes_to_long(message.encode())
    c = pow(m, e, n)
    print(f"Here is your encrypted message: {c}")
    print(f"c = {c}")
    print("Here is the public key for your reference:")
    print(f"n = {n}")
    print(f"e = {e}")
    
print("Thank you for encrypting with us!")
print("In order to guarantee the security of your data, we will now let you view the encrypted flag.")
x=input("Would you like to view it? (yes or no) ")

if x.lower() == "yes":
    with open("flag.txt", "r") as f:
        flag = f.read().strip()
    m = bytes_to_long(flag.encode())
    n = p*r
    c = pow(m, e, n)
    print(f"Here is the encrypted flag: {c}")
    print("Here is the public key for your reference:")
    print(f"n = {n}")