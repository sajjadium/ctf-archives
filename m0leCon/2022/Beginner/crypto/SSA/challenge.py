# The following imports are from the pycryptodome library
from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from secret import message
import random
import os


if __name__ == '__main__':
    print('Welcome to the Secret Service Agency, the most secret agency in the world!')
    print('We have found out that there is a mole between our specialized agents. One of our most capable men, Agent Platypus, has found out a communication between him and his accomplice encrypted with a key that they shared using the Diffie Hellman protocol beforehead.')
    print('Can you find out the key used to encrypt the message and decrypt it, knowing that the message has been encrypted with AES-CBC and the key has been derivated with "s.to_bytes(16, \'little\')", where "s" is the shared secret between the two? We hope to find out who the mole and his accomplice are!')
    print('Here it is the communication we have been able to intercept:')
    print()

    g = 2
    p = getPrime(64)
    a = random.randint(1, p-1)
    A = pow(g, a, p)

    print('Mole:')
    print('g =', g)
    print('p =', p)
    print('A =', A)
    print()

    b = random.randint(1, p-1)

    print('Accomplice:')
    print('B =', pow(g, b, p))
    print()

    key = pow(A, b, p).to_bytes(16, 'little')
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    print('Mole:')
    print('IV =', iv.hex())
    print(
        'Message =',
        cipher.encrypt(pad(message.encode(), AES.block_size)).hex()
    )
