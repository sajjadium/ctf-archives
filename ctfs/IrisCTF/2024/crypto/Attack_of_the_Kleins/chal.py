import secrets

def ksa(key):
    buf = []
    for i in range(256):
        buf.append(i)
    
    j = 0
    for i in range(256):
        j = (j + buf[i] + key[i % len(key)]) % 256
        buf[i], buf[j] = buf[j], buf[i]
    
    return buf

def pgra(buf):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (buf[i] + j) % 256
        buf[i], buf[j] = buf[j], buf[i]
        yield buf[(buf[i] + buf[j]) % 256]

def rc4(buf, key, iv):
    buf = bytearray(buf, 'latin-1')
    sched = ksa(iv + key)
    keystream = pgra(sched)

    for i in range(len(buf)):
        buf[i] ^= next(keystream)
    
    return buf

ctr = 0
def generate_new_iv(old_iv):
    global ctr
    ctr += 1
    new_iv = []

    # add to it for extra confusion
    for i in range(8):
        old_iv[i] = (old_iv[i] + 1) & 0xff
        if old_iv[i] == 0:
            old_iv[i] = 0
        else:
            break
    
    for i in range(len(old_iv)):
        off = (secrets.randbits(8) - 128) // 2
        new_iv.append((old_iv[i] + off) & 0xff)
    
    return bytes(new_iv)

def main():
    iv = bytearray(secrets.token_bytes(8))
    key = bytearray(secrets.token_bytes(16))
    free_encrypts = 1000
    
    print("Welcome to EncryptIt!")
    print(f"1. Encrypt message ({free_encrypts} free encrypts remaining)")
    print(f"2. Print encrypted flag")
    while True:
        choice = input("? ")
        if choice == "1":
            if free_encrypts <= 0:
                print("No more free encrypts remaining")
                continue
            
            msg = input("Message? ")
            new_iv = generate_new_iv(iv)
            crypted = rc4(msg, key, new_iv)
            print(new_iv.hex() + crypted.hex())
            free_encrypts -= 1
        elif choice == "2":
            msg = "Here is the flag: irisctf{fake_flag}"
            new_iv = generate_new_iv(iv)
            crypted = rc4(msg, key, iv)
            print(crypted.hex())

main()
