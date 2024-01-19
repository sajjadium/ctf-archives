from random import randint

def gen_key():

    a, b, c, d = randint(3 * 64), randint(4 * 64), randint(5 * 64), randint(6 * 64)

    e = a * b - 1
    f = c * e + a + e
    g = d * e + b * f
    h = c * d * e + a * d + c * b + g * g

    public_key = (h, f)
    private_key = g
    key = (public_key, private_key)

    return key

def encrypt(m, public_key):
    c = (m * public_key[1]) % public_key[0]
    return c

def decrypt(c, public_key, private_key):
    m = (c * private_key) % public_key[0]
    return m