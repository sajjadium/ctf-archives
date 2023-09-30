import hashlib
from sys import exit

flag = '8f163b472e2164f66a5cd751098783f9'

str = input("Enter the flag\n")
str = hashlib.md5(str.encode())

if str.digest().hex() == flag:
    print("Congrats! You got the flag!")
else:
    print("Nope. Try again!")

exit()
