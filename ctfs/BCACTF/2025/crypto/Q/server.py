from os import urandom
from secrets import randbelow

secret_str = urandom(16).hex()
secret = [ord(char) for char in secret_str]

for _ in range(5000):
    encoded = [value + randbelow(2000) for value in secret]
    print(encoded)

user_secret = input('What is the secret? ')

if user_secret == secret_str:
    with open('flag.txt', 'r') as file:
        print(file.read())
else:
    print('Wrong :(')
