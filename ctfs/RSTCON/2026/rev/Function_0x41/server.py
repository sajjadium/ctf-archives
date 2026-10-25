import socketserver
import struct

FLAG = b"rstcon{REDACTED}"
UNIT_ID = 0x01
CUSTOM_FC = 0x41

BREADCRUMB = [ord('0'), ord('x'), ord('4'), ord('1')]

def transform(seed: int) -> int:

    return (((seed ^ 0x1F3D) * 0x0101) + 0x2027) & 0xFFFF

def mbap(tid, proto, unit, pdu):
    return struct.pack(">HHHB", tid, proto, len(pdu) + 1, unit) + pdu

def exception(fc, code):
    return struct.pack(">BB", fc | 0x80, code)

def handle_pdu(pdu: bytes) -> bytes:
    fc = pdu[0]

    if fc == 0x03:
        if len(pdu) < 5:
            return exception(fc, 0x03)
        addr, qty = struct.unpack(">HH", pdu[1:5])
        vals = []
        for i in range(qty):
            r = addr + i
            vals.append(BREADCRUMB[r] if 0 <= r < len(BREADCRUMB) else 0)
        body = b"".join(struct.pack(">H", v) for v in vals)
        return struct.pack(">BB", 0x03, len(body)) + body

    if fc == CUSTOM_FC:
        if len(pdu) < 5:
            return exception(fc, 0x03)
        seed, guess = struct.unpack(">HH", pdu[1:5])
        if guess == transform(seed):
            return struct.pack(">BB", CUSTOM_FC, 0x00) + FLAG
        return struct.pack(">BB", CUSTOM_FC, 0x01)

    return exception(fc, 0x01)

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        buf = b""
        while True:
            chunk = self.request.recv(1024)
            if not chunk:
                break
            buf += chunk

            while len(buf) >= 7:
                tid, proto, length, unit = struct.unpack(">HHHB", buf[:7])
                if len(buf) < 6 + length:
                    break
                pdu = buf[7:6 + length]
                buf = buf[6 + length:]
                resp_pdu = handle_pdu(pdu)
                self.request.sendall(mbap(tid, proto, unit, resp_pdu))

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 502
    print(f"[*] Function 0x41 device listening on {HOST}:{PORT}")
    Server((HOST, PORT), Handler).serve_forever()
