from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

with open("flag.txt", "rb") as f:
    flag = f.read()

key = os.urandom(16)

# Efficient service for pre-generating personal, romantic, deeply heartfelt white day gifts for all the people who sent you valentines gifts
for _ in range(1024):

    # Which special someone should we prepare a truly meaningful gift for? 
    recipient = input("Recipient name: ")

    # whats more romantic than the abstract notion of a securely encrypted flag?
    romantic_message = f'Dear {recipient}, as a token of the depth of my feelings, I gift to you that which is most precious to me. A {flag}'
    
    aes = AES.new(key, AES.MODE_CBC, iv=b'preprocessedlove')

    print(f'heres a thoughtful and unique gift for {recipient}: {aes.decrypt(pad(romantic_message.encode(), AES.block_size)).hex()}')