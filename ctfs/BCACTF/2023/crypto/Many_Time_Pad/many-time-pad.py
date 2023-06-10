from Crypto.Util.number import *
secret_key = open("secret_key.txt", "rb").read()

def enc(bstr):
    return long_to_bytes(bytes_to_long(bstr) ^ bytes_to_long(secret_key))

# gotta encode my grocery list
groceries = b"I need to buy 15 eggs, 1.7 kiloliters of milk, 11000 candles, 12 cans of asbestos-free cereal, and 0.7 watermelons."
out = open("grocery-list.out", "wb")
out.write(enc(groceries))
out.close()

# gotta encode my flag
out = open("many-time-pad.out", "wb")
out.write(enc(open("flag.txt", "rb").read()))
out.close()