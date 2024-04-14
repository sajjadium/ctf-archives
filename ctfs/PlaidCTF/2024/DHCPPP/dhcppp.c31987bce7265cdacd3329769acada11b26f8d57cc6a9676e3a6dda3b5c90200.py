import time, zlib
import secrets
import hashlib
import requests
from Crypto.Cipher import ChaCha20_Poly1305
import dns.resolver

CHACHA_KEY = secrets.token_bytes(32)
TIMEOUT = 1e-1

def encrypt_msg(msg, nonce):
    # In case our RNG nonce is repeated, we also hash
    # the message in. This means the worst-case scenario
    # is that our nonce reflects a hash of the message
    # but saves the chance of a nonce being reused across
    # different messages
    nonce = sha256(msg[:32] + nonce[:32])[:12]

    cipher = ChaCha20_Poly1305.new(key=CHACHA_KEY, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(msg)

    return ct+tag+nonce

def decrypt_msg(msg):
    ct = msg[:-28]
    tag = msg[-28:-12]
    nonce = msg[-12:]

    cipher = ChaCha20_Poly1305.new(key=CHACHA_KEY, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)

    return pt

def calc_crc(msg):
    return zlib.crc32(msg).to_bytes(4, "little")

def sha256(msg):
    return hashlib.sha256(msg).digest()

RNG_INIT = secrets.token_bytes(512)

class DHCPServer:
    def __init__(self):
        self.leases = []
        self.ips = [f"192.168.1.{i}" for i in range(3, 64)]
        self.mac = bytes.fromhex("1b 7d 6f 49 37 c9")
        self.gateway_ip = "192.168.1.1"

        self.leases.append(("192.168.1.2", b"rngserver_0", time.time(), []))

    def get_lease(self, dev_name):
        if len(self.ips) != 0:
            ip = self.ips.pop(0)
            self.leases.append((ip, dev_name, time.time(), []))
        else:
            # relinquish the oldest lease
            old_lease = self.leases.pop(0)
            ip = old_lease[0]
            self.leases.append((ip, dev_name, time.time(), []))

        pkt = bytearray(
            bytes([int(x) for x in ip.split(".")]) +
            bytes([int(x) for x in self.gateway_ip.split(".")]) +
            bytes([255, 255, 255, 0]) +
            bytes([8, 8, 8, 8]) +
            bytes([8, 8, 4, 4]) +
            dev_name +
            b"\x00"
        )

        pkt = b"\x02" + encrypt_msg(pkt, self.get_entropy_from_lavalamps()) + calc_crc(pkt)

        return pkt

    def get_entropy_from_lavalamps(self):
        # Get entropy from all available lava-lamp RNG servers
        # Falling back to local RNG if necessary
        entropy_pool = RNG_INIT

        for ip, name, ts, tags in self.leases:
            if b"rngserver" in name:
                try:
                    # get entropy from the server
                    output = requests.get(f"http://{ip}/get_rng", timeout=TIMEOUT).text
                    entropy_pool += sha256(output.encode())
                except:
                    # if the server is broken, get randomness from local RNG instead
                    entropy_pool += sha256(secrets.token_bytes(512))

        return sha256(entropy_pool)

    def process_pkt(self, pkt):
        assert pkt is not None

        src_mac = pkt[:6]
        dst_mac = pkt[6:12]
        msg = pkt[12:]

        if dst_mac != self.mac:
            return None

        if src_mac == self.mac:
            return None

        if len(msg) and msg.startswith(b"\x01"):
            # lease request
            dev_name = msg[1:]
            lease_resp = self.get_lease(dev_name)
            return (
                self.mac +
                src_mac + # dest mac
                lease_resp
            )
        else:
            return None

class FlagServer:
    def __init__(self, dhcp):
        self.mac = bytes.fromhex("53 79 82 b5 97 eb")
        self.dns = dns.resolver.Resolver()
        self.process_pkt(dhcp.process_pkt(self.mac+dhcp.mac+b"\x01"+b"flag_server"))

    def send_flag(self):
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
        curl("example.com", f"/{flag}", self.dns)

    def process_pkt(self, pkt):
        assert pkt is not None

        src_mac = pkt[:6]
        dst_mac = pkt[6:12]
        msg = pkt[12:]

        if dst_mac != self.mac:
            return None

        if src_mac == self.mac:
            return None

        if len(msg) and msg.startswith(b"\x02"):
            # lease response
            pkt = msg[1:-4]
            pkt = decrypt_msg(pkt)
            crc = msg[-4:]
            assert crc == calc_crc(pkt)

            self.ip = ".".join(str(x) for x in pkt[0:4])
            self.gateway_ip = ".".join(str(x) for x in pkt[4:8])
            self.subnet_mask = ".".join(str(x) for x in pkt[8:12])
            self.dns1 = ".".join(str(x) for x in pkt[12:16])
            self.dns2 = ".".join(str(x) for x in pkt[16:20])
            self.dns.nameservers = [self.dns1, self.dns2]
            assert pkt.endswith(b"\x00")

            print("[FLAG SERVER] [DEBUG] Got DHCP lease", self.ip, self.gateway_ip, self.subnet_mask, self.dns1, self.dns2)

            return None

        elif len(msg) and msg.startswith(b"\x03"):
            # FREE FLAGES!!!!!!!
            self.send_flag()
            return None

        else:
            return None

def curl(url, path, dns):
    ip = str(dns.resolve(url).response.resolve_chaining().answer).strip().split(" ")[-1]
    url = "http://" + ip
    print(f"Sending flage to {url}")
    requests.get(url + path)

if __name__ == "__main__":
    dhcp = DHCPServer()
    flagserver = FlagServer(dhcp)

    while True:
        pkt = bytes.fromhex(input("> ").replace(" ", "").strip())

        out = dhcp.process_pkt(pkt)
        if out is not None:
            print(out.hex())

        out = flagserver.process_pkt(pkt)
        if out is not None:
            print(out.hex())

