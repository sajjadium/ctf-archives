from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long

with open("flag.txt", "rb") as f:
    FLAG = f.read()

n = bytes_to_long(FLAG)

#make sure i have a big modulus
while n.bit_length() < 2048:
    n *= n

def encrypt(m1, m2):
    e = getPrime(256)
    assert m1.bit_length() >= 1600 and long_to_bytes(m1).startswith(b"SEE{"), 'first message must be at least 1600 bits and begin with "SEE{"'
    assert 500 <= m2.bit_length() <= 600, 'second message must be within 500 to 600 bits'

    return pow(m1, e, n), pow(m2, e, n)


def main():
    try:
        m1 = int(input("Message 1 (as integer) : ").strip())
        m2 = int(input("Message 2 (as integer) : ").strip())
        c1, c2 = encrypt(m1, m2)
        print(f"\nCiphers: \n{[c1,c2]}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

