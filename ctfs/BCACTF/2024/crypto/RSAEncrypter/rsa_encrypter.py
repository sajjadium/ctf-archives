from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes


message = open("./flag.txt").read().encode('utf-8')  


def encode():
    n = getPrime(512)*getPrime(512)
    ciphertext = pow(bytes_to_long(message), 3, n)
    return (ciphertext, n)

print("Return format: (ciphertext, modulus)")
print(encode())
sent = input("Did you recieve the message? (y/n) ")
while sent=='n':
    print(encode())
    sent = input("How about now? (y/n) ")
print("Message acknowledged.")