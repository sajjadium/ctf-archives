from Crypto.Cipher import AES
import binascii, os

key = b"3153153153153153"
iv =  os.urandom(16)

plaintext = open('message.txt', 'rb').read().strip()

cipher = AES.new(key, AES.MODE_CBC, iv)

encrypted_flag = open('message.enc', 'wb')
encrypted_flag.write(binascii.hexlify(cipher.encrypt(plaintext)))
encrypted_flag.close()
