from Crypto.Util import number
from Crypto.Util.number import long_to_bytes, bytes_to_long


def getPrime():
    # Note: to reduce server workload, we actually read from a precalculated list of primes.
    # This doesn't meaningfully change the challenge.
    p = number.getPrime(285)
    return p


def encrypt():
    pt = bytes_to_long(b"RITSEC{not_the_real_flag}")
    phi = 65537
    e = 65537

    while phi % e == 0:
        p = getPrime()
        q = getPrime()

        n = p * q
        phi = (p-1) * (q-1)
    
    d = pow(e, -1, phi)
    ct = pow(pt, e, n)
    print("m="  + str(ct))
    print("phi=" + str(phi))
    print("e=" + str(e))


print("Welcome to my rsa service. I'm not quite sure I got rsa right, but I did my best")
i = 0
while True:
    print("Enter 1 to get an encrypted message or 2 to exit")
    msg = input("")
    if msg == "1":
        encrypt()
    elif msg == "2" or i > 49000:
        break
    else:
        print("I didn't get that")
    i += 1
