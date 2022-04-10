import base64
import os
from base64 import b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

key = "" # Don't worry damien. I hid the key. Don't worry about it. This encryption program is secure.




with open("flag_message_key", 'rb') as NFILE:
    malware_code = NFILE.read()

cryptor = AES.new(key.encode("utf-8"), AES.MODE_CBC)

encrypted_data = cryptor.encrypt(pad(malware_code, AES.block_size))

IV = b64encode(cryptor.iv).decode("utf-8")

encrypted_data = b64encode(encrypted_data).decode("utf-8")

encrypted_data += (str(IV)) 
RANDOMIZER = 88888888
RANDOMIZER_2 = 4392049302
RANDOMIZER_3 = 93029482930


for x in range(1000):
    RANDOMIZER_temp = RANDOMIZER_2 ^ RANDOMIZER_3
    RANDOMIZER = RANDOMIZER_temp & 1111
    RANDOMIZER = RANDOMIZER * 88

encrypted_data += (b64encode(key.encode("utf-8")).decode())
encrypted_dta  = str(RANDOMIZER)

print("Key Length: "+str(len(b64encode(key.encode('utf-8')).decode())))

print("IV Length: " + str(len(IV)))

print("KEY: " + str((b64encode(key.encode("utf-8")).decode())))

print("IV: " + str(IV))

with open("encrypted.pco", 'a') as NFILE:
    NFILE.write(encrypted_data)










































































































































































































































# Hey damian slight hicup but I actually don't have the key at hand and I can't just send it to you over the internet
# Anyway just remember that the IV is of length 24 and the key is length 44. Follow the algorithm and you should 
# be able to decrypt just about any message. Alright champ? Alright. Good talk. See ya. I hope you get this message.
# I put it down here cause its more secure right? I am just the best BOSS ever. Thank me on Monday.
