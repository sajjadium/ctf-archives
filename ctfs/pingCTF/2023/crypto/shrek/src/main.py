import os
from shrek import Shrek

shrek = Shrek()
FLAG = os.environ.get("FLAG", "ping{FAKE}")

for i in range(10):
    plainText = shrek.generatePlainText()
    print(f'Ciphertext: {shrek.encrypt(plainText)}')
    guess = input('Can you guess plaintext?: ')

    if guess == plainText:
        print(f'Congratulations, your reward: {FLAG}')
    else:
        print('Try harder!')
print('noob')
