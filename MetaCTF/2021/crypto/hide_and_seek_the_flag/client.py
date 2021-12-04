import socket, sys, select, gmpy2

def establish_communication(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        keys = []
        while True:
            active = select.select([s, sys.stdin], [], [])[0]
            if s in active:
                buf = s.recv(260)
                if buf[0] == 0:
                    pub = int.from_bytes(buf[1:4], byteorder="big")
                    p = int.from_bytes(buf[4:132], byteorder="big")
                    q = int.from_bytes(buf[132:260], byteorder="big")
                    priv = gmpy2.invert(pub, (p-1) * (q-1))
                    keys += [(int(priv), p * q)]
                else:
                    msg = int.from_bytes(buf[1:], byteorder="big")
                    msg = pow(msg, keys[0][0], keys[0][1])
                    keys = keys[1:]
                    print(msg.to_bytes(256, byteorder="big"))
            if sys.stdin in active:
                buf = int.from_bytes(sys.stdin.read(250).encode("utf-8"), byteorder="big")
                s.send(b"\x00")
                enckey = s.recv(260)
                pub = int.from_bytes(enckey[1:4], byteorder="big")
                mod = int.from_bytes(enckey[4:260], byteorder="big")
                enc = pow(buf, pub, mod)
                s.send(b"\x01" + enc.to_bytes(259, byteorder="big"))

establish_communication(sys.argv[1], int(sys.argv[2]))
