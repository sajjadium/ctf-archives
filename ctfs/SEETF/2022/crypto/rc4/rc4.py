import os

def rc4(key:bytes, pt:bytes) -> bytes:
    
    s = [*range(0x100)]
    j = 0
    for i in range(len(key)):
        j = (j + s[i] + key[i]) & 0xff
        s[i], s[j] = s[j], s[i]
    
    i = 0
    j = 0
    ret = []
    for c in pt:
        i = (i + 1) & 0xff
        j = (j + s[i]) & 0xff
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) & 0xff]
        ret.append(k^c)

    return bytes(ret)

def gen_rand_key():
    return os.urandom(96).hex().encode()

if __name__ == "__main__":

    from secret import secret
    pos_flag = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    assert all(f in pos_flag for f in secret)
    
    ct = b"".join(rc4(gen_rand_key(), secret) for _ in range(0x100000))
    open("ct", "wb").write(ct)
    print(f"Flag: SEE{{{secret.decode()}}}")