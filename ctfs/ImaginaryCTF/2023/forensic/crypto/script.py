from Crypto.PublicKey import RSA

t = open('private.pem', "r").read()
key = RSA.importKey(t)

input()
