import gmpy2
import random
import socket
import select

sockets = []

def get_rsa_info():
    p = gmpy2.next_prime(random.getrandbits(1024))
    q = gmpy2.next_prime(random.getrandbits(1024))
    e = 65537
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    return (e, int(p), int(q))

def establish_communication(port):
    global sockets
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(2)
        while len(sockets) != 2:
            c, addr = s.accept()
            sockets += [c]
        while True:
            active = select.select(sockets, [], [])[0]
            for s in active:
                buf = s.recv(260)
                if(buf[0] == 0):
                    e, p, q = get_rsa_info()
                    send_buf = b"\x00"
                    send_buf += e.to_bytes(3, "big")
                    send_buf += p.to_bytes(128, "big")
                    send_buf += q.to_bytes(128, "big")
                    print("Sending ", b"\x00" + e.to_bytes(3, "big") + (p * q).to_bytes(256, "big"))
                    s.send(b"\x00" + e.to_bytes(3, "big") + (p * q).to_bytes(256, "big"))
                    for s1 in sockets:
                        if s1 != s:
                            s1.send(send_buf)
                else:
                    for s1 in sockets:
                        if s1 != s:
                            s1.send(buf)
establish_communication(1337)
