import textwrap
from binascii import crc32
from Crypto.Util.number import getPrime

p, q = getPrime(1024), getPrime(1024)
n = p*q
e = 65537
d = pow(e, -1, (p-1)*(q-1))

PASSWORD = b"give me the flag!!!"

print("--------------------------------------------------------------")
print("               Welcome to the secure signing app!             ")
print("  I will sign whatever you want, except the secret password.  ")
print("--------------------------------------------------------------")
print()
print("--------------------------------------------------------------")
print("\n".join(textwrap.wrap(f"{n = }", len("-------------------------------------------------------------"))))
print("--------------------------------------------------------------")
print()

while True:
  print("1. Sign")
  print("2. Get flag")
  choice = int(input())

  if choice == 1:
    print("Enter message:")
    message = input().encode()
    # crc32 is secure and has no collisions, but just in case
    if message == PASSWORD or crc32(message) == crc32(PASSWORD):
      print("Stop this trickery!")
      exit()
    print("Signature:", pow(crc32(message), d, n))
  elif choice == 2:
    print("Enter the signature for the password:")
    s = int(input())
    if pow(s, e, n) == crc32(PASSWORD):
      print("You win! The flag is", open("flag.txt").read())
      exit()
    else:
      print("Wrong.")
      exit()
