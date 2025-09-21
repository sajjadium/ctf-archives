import socket, os, time, random, binascii
fd=os.open("/opt/app/random", os.O_RDONLY)
def seed_once():
    data=b""
    try:
        data=os.read(fd, 4096)
    except:
        data=b""
    if len(data)>=2048:
        return int.from_bytes(data,"big")
    return (int(time.time()) ^ os.getpid()) 

def xor_bytes(a,b):
    return bytes(x^y for x,y in zip(a,b))

def handle_client(c, flag):
    seed=seed_once()
    rng=random.Random(seed)
    ks=bytearray()
    while len(ks)<len(flag):
        ks.extend(rng.getrandbits(8).to_bytes(1,"big"))
    ct=xor_bytes(flag, ks[:len(flag)])
    leak=[rng.getrandbits(32) for _ in range(3)]
    out={
        "ciphertext_hex": binascii.hexlify(ct).decode(),
        "leak32": leak,
        "pid": os.getpid()

    }
    c.sendall((str(out)+"\n").encode())

def main():
    flag=os.environ.get("FLAG","you ran this locally, duh").encode()
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0",5000))
    s.listen(64)
    while True:
        c,a=s.accept()
        try:
            handle_client(c, flag)
        finally:
            c.close()

if __name__=="__main__":
    main()
